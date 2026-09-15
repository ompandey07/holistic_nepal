from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password, make_password
from django.contrib import messages
from django.urls import reverse
from django.core.files.storage import default_storage
import json
import re

#!- IMPORT USERS MODELS AND SECURITY WRAPPERS
from users.models import EmployeeSetup, PublicUserProfile
from users.wrapper import advance_security_wrapper, check_suspicious_input, get_client_ip, sanitize_input_string


#!- PASSWORD VERIFICATION HELPER
def verify_password(raw_password, stored_password):
    #!- VERIFY HASHED OR PLAIN TEXT PASSWORDS
    if not stored_password or not raw_password:
        return False
    try:
        if check_password(raw_password, stored_password):
            return True
    except Exception:
        pass
    return raw_password == stored_password


#!- LOGIN CLASS BASED VIEW
class LoginView(View):

    def get(self, request):
        #!- RENDER LOGIN HTML TEMPLATE
        return render(request, 'auth/login.html')

    def post(self, request):
        #!- EXTRACT CREDENTIALS FROM POST OR JSON BODY ROBUSTLY
        email = (request.POST.get('email') or request.POST.get('username') or '').strip()
        password = request.POST.get('password') or ''

        if not email or not password:
            try:
                if request.body:
                    body_data = json.loads(request.body.decode('utf-8'))
                    if isinstance(body_data, dict):
                        email = (body_data.get('email') or body_data.get('username') or '').strip()
                        password = body_data.get('password') or ''
            except Exception:
                pass

        if not email or not password:
            return JsonResponse({'status': 'error', 'message': 'Email and password are required.'}, status=400)

        #!- 1. CHECK SUPERUSER / DJANGO AUTHENTICATION
        django_user = authenticate(request, username=email, password=password)
        if django_user is None and '@' in email:
            from django.contrib.auth.models import User
            user_obj = User.objects.filter(email__iexact=email).first()
            if user_obj and verify_password(password, user_obj.password):
                django_user = user_obj

        if django_user and django_user.is_active:
            login(request, django_user)
            request.session['is_employee_or_superuser'] = True
            request.session['user_role'] = 'SUPERUSER' if django_user.is_superuser else 'ADMIN'
            return JsonResponse({
                'status': 'success',
                'message': 'Login successful. Redirecting to dashboard...',
                'redirect_url': reverse('admin_dashboard')
            })

        #!- 2. CHECK EMPLOYEE SETUP MODEL
        employee = EmployeeSetup.objects.filter(EMPLOYEE_EMAIL__iexact=email).first()
        if not employee:
            employee = EmployeeSetup.objects.filter(EMPLOYEE_EMAIL=email).first()

        if employee and verify_password(password, employee.EMPLOYEE_PASSWORD):
            request.session['employee_id'] = employee.id
            request.session['employee_name'] = employee.EMPLOYEE_FULL_NAME
            request.session['employee_role'] = employee.EMPLOYEE_ROLE
            request.session['is_employee_or_superuser'] = True
            return JsonResponse({
                'status': 'success',
                'message': 'Welcome back! Redirecting to dashboard...',
                'redirect_url': reverse('admin_dashboard')
            })

        #!- 3. CHECK PUBLIC USER PROFILE MODEL
        public_user = PublicUserProfile.objects.filter(PUBLIC_USER_EMAIL__iexact=email).first()
        if not public_user:
            public_user = PublicUserProfile.objects.filter(PUBLIC_USER_EMAIL=email).first()

        if public_user and verify_password(password, public_user.PUBLIC_USER_PASSWORD):
            request.session['public_user_id'] = public_user.id
            request.session['public_user_name'] = public_user.PUBLIC_USER_FULL_NAME
            request.session['role'] = 'PUBLIC_USER'
            request.session['is_employee_or_superuser'] = False
            return JsonResponse({
                'status': 'success',
                'message': 'i am public',
                'role': 'PUBLIC_USER'
            })

        #!- INVALID CREDENTIALS RESPONSE
        return JsonResponse({
            'status': 'error',
            'message': 'Incorrect email or password.'
        }, status=400)


#!- LOGOUT CLASS BASED VIEW
class LogoutView(View):

    def get(self, request):
        #!- FLUSH SESSION AND LOGOUT USER
        logout(request)
        request.session.flush()
        messages.success(request, "Logged out successfully.")
        return redirect('login')

    def post(self, request):
        #!- AJAX LOGOUT RESPONSE
        logout(request)
        request.session.flush()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
            return JsonResponse({
                'status': 'success',
                'message': 'Logged out successfully.',
                'redirect_url': reverse('login')
            })
        messages.success(request, "Logged out successfully.")
        return redirect('login')


#!- PUBLIC USER REGISTER CLASS BASED VIEW
class PublicRegisterView(View):

    #!- STRICT EMAIL REGEX: MUST HAVE REAL-LOOKING DOMAIN (NO test123 ETC.)
    _EMAIL_RE = re.compile(
        r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'
    )
    #!- PHONE: DIGITS ONLY, MAX 10
    _PHONE_RE = re.compile(r'^\d{1,10}$')

    def _validate_email(self, email):
        """#! VALIDATE EMAIL FORMAT AND REJECT OBVIOUSLY FAKE DOMAINS."""
        email = email.strip().lower()
        if not self._EMAIL_RE.match(email):
            return False, 'Enter a valid email address (e.g. you@gmail.com).'
        #!- REJECT PLACEHOLDER-STYLE LOCAL PARTS (test, user123, fake, etc.)
        local_part = email.split('@')[0]
        fake_patterns = re.compile(
            r'^(test|fake|demo|dummy|sample|user\d*|admin\d*|noreply|no-reply|example|abc\d*|xyz\d*)$',
            re.IGNORECASE
        )
        if fake_patterns.match(local_part):
            return False, 'Please use your real email address.'
        #!- REJECT OBVIOUSLY FAKE TLD-LESS DOMAINS
        domain = email.split('@')[1]
        if '.' not in domain:
            return False, 'Enter a valid email address with a proper domain.'
        return True, ''

    def get(self, request):
        #!- RENDER REGISTER HTML TEMPLATE
        return render(request, 'auth/register.html')

    def post(self, request):
        #!- EXTRACT FORM DATA
        full_name    = (request.POST.get('full_name') or '').strip()
        email        = (request.POST.get('email') or '').strip().lower()
        mobile_no    = (request.POST.get('mobile_no') or '').strip()
        address      = (request.POST.get('address') or '').strip()
        password     = request.POST.get('password') or ''
        confirm_pass = request.POST.get('confirm_password') or ''
        profile_img  = request.FILES.get('profile_image')

        errors = {}

        #!- FULL NAME VALIDATION
        if not full_name:
            errors['full_name'] = 'Full name is required.'
        elif len(full_name) < 2:
            errors['full_name'] = 'Full name must be at least 2 characters.'

        #!- EMAIL VALIDATION
        if not email:
            errors['email'] = 'Email address is required.'
        else:
            ok, msg = self._validate_email(email)
            if not ok:
                errors['email'] = msg
            elif PublicUserProfile.objects.filter(PUBLIC_USER_EMAIL__iexact=email).exists():
                errors['email'] = 'An account with this email already exists.'

        #!- MOBILE NUMBER VALIDATION
        if not mobile_no:
            errors['mobile_no'] = 'Mobile number is required.'
        elif not self._PHONE_RE.match(mobile_no):
            if len(mobile_no) > 10:
                errors['mobile_no'] = 'Mobile number must not exceed 10 digits.'
            else:
                errors['mobile_no'] = 'Mobile number must contain digits only (max 10 digits).'

        #!- ADDRESS VALIDATION
        if not address:
            errors['address'] = 'Address is required.'

        #!- PASSWORD VALIDATION
        if not password:
            errors['password'] = 'Password is required.'
        elif len(password) < 6:
            errors['password'] = 'Password must be at least 6 characters.'

        #!- CONFIRM PASSWORD
        if not confirm_pass:
            errors['confirm_password'] = 'Please confirm your password.'
        elif password and confirm_pass and password != confirm_pass:
            errors['confirm_password'] = 'Passwords do not match.'

        if errors:
            return JsonResponse({'status': 'error', 'errors': errors, 'message': 'Please fix the highlighted fields.'}, status=400)

        #!- CAPTURE CLIENT IP
        client_ip = get_client_ip(request)

        #!- HASH THE PASSWORD
        hashed_password = make_password(password)

        #!- CREATE THE PUBLIC USER PROFILE
        try:
            new_user = PublicUserProfile(
                PUBLIC_USER_FULL_NAME=full_name,
                PUBLIC_USER_EMAIL=email,
                PUBLIC_USER_MOBILE_NO=mobile_no,
                PUBLIC_USER_ADDRESS=address,
                PUBLIC_USER_IP=client_ip,
                PUBLIC_USER_PASSWORD=hashed_password,
            )
            #!- ATTACH PROFILE IMAGE IF PROVIDED
            if profile_img:
                new_user.PUBLIC_USER_PROFILE_IMAGE = profile_img
            new_user.save()
        except Exception as exc:
            return JsonResponse({'status': 'error', 'message': f'Registration failed: {exc}'}, status=500)

        return JsonResponse({
            'status': 'success',
            'message': 'Registration successful! Redirecting to login…',
            'redirect_url': reverse('login')
        })
