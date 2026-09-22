from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password, make_password
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.storage import default_storage
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache
import json
import re
import logging

logger = logging.getLogger(__name__)

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
            #!- CREATE OR GET DJANGO USER FOR PUBLIC USER
            try:
                django_user = User.objects.get(email=public_user.PUBLIC_USER_EMAIL)
            except User.DoesNotExist:
                # Create Django user for public user
                django_user = User.objects.create_user(
                    username=public_user.PUBLIC_USER_EMAIL,
                    email=public_user.PUBLIC_USER_EMAIL,
                    password=public_user.PUBLIC_USER_PASSWORD
                )
            
            # 1. Defensively snapshot guest session cart before login session cycle
            guest_session_cart = dict(request.session.get('cart', {}))

            #!- LOGIN THE DJANGO USER
            login(request, django_user)
            request.session['public_user_id'] = public_user.id
            request.session['public_user_name'] = public_user.PUBLIC_USER_FULL_NAME
            request.session['role'] = 'PUBLIC_USER'
            request.session['is_employee_or_superuser'] = False

            # 2. Restore guest session cart into cycled session if needed
            if guest_session_cart:
                current_cart = request.session.get('cart', {})
                for k, v in guest_session_cart.items():
                    if k not in current_cart or not current_cart[k]:
                        current_cart[k] = v
                request.session['cart'] = current_cart
                request.session.modified = True

            # 3. Merge guest session cart into user account cart
            try:
                from core.cart import Cart
                cart = Cart(request)
                cart.merge_session_cart(public_user)
            except Exception:
                pass

            # Determine return destination: check next query param or payload
            next_url = (request.GET.get('next') or request.POST.get('next') or '').strip()
            if not next_url:
                try:
                    if request.body:
                        b_data = json.loads(request.body.decode('utf-8'))
                        if isinstance(b_data, dict):
                            next_url = (b_data.get('next') or '').strip()
                except Exception:
                    pass

            redirect_target = reverse('user_dashboard')
            if next_url and next_url.startswith('/') and not next_url.startswith('//'):
                redirect_target = next_url

            return JsonResponse({
                'status': 'success',
                'message': 'Welcome back! Redirecting...',
                'redirect_url': redirect_target
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


# ==============================================================================
# -- PASSWORD RESET TOKEN GENERATOR (SCOPED STRICTLY TO PublicUserProfile) -----
# ==============================================================================
class PublicUserPasswordResetTokenGenerator(PasswordResetTokenGenerator):
    """
    Subclassed from Django's built-in PasswordResetTokenGenerator.
    Specifically keyed to PublicUserProfile's primary key, password hash,
    and update timestamp for secure one-time usage and automatic expiration.
    """
    def _make_hash_value(self, user, timestamp):
        updated_ts = ''
        if hasattr(user, 'PUBLIC_USER_UPDATED_AT') and user.PUBLIC_USER_UPDATED_AT:
            updated_ts = str(user.PUBLIC_USER_UPDATED_AT.timestamp())
        return f"{user.pk}{user.PUBLIC_USER_PASSWORD}{updated_ts}{timestamp}"

public_user_token_generator = PublicUserPasswordResetTokenGenerator()


def check_password_reset_rate_limit(ip, email, limit=5, timeout=3600):
    """
    Rate limiting: max `limit` requests per IP and per email per `timeout` seconds (default: 5/hr).
    Returns True if rate limit is exceeded, False otherwise.
    """
    clean_email = (email or '').strip().lower()
    ip_key = f"pwd_reset_rate_ip:{ip}"
    email_key = f"pwd_reset_rate_email:{clean_email}"

    ip_count = cache.get(ip_key, 0)
    email_count = cache.get(email_key, 0) if clean_email else 0

    if ip_count >= limit or email_count >= limit:
        return True

    cache.set(ip_key, ip_count + 1, timeout)
    if clean_email:
        cache.set(email_key, email_count + 1, timeout)
    return False


class PasswordResetRequestView(View):
    """
    Customer password reset request view.
    Accepts GET (renders form) and POST (handles email submission).
    Rate-limited to 5 requests per IP/email per hour.
    Scoped STRICTLY to PublicUserProfile.
    """
    def get(self, request):
        return render(request, 'auth/password_reset.html')

    def post(self, request):
        email = ''
        if request.content_type == 'application/json' or request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                data = json.loads(request.body.decode('utf-8')) if request.body else {}
                email = data.get('email', '')
            except Exception:
                pass
        if not email:
            email = request.POST.get('email', '')

        email = email.strip().lower()
        client_ip = get_client_ip(request)

        # 1. Rate limiting check
        if check_password_reset_rate_limit(client_ip, email, limit=5, timeout=3600):
            msg = "Too many password reset attempts. Please wait an hour before trying again."
            if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
                return JsonResponse({'status': 'error', 'message': msg}, status=429)
            messages.error(request, msg)
            return render(request, 'auth/password_reset.html', {'error': msg})

        if not email:
            msg = "Please enter a valid email address."
            if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
                return JsonResponse({'status': 'error', 'message': msg}, status=400)
            return render(request, 'auth/password_reset.html', {'error': msg})

        # 2. STRICTLY search PublicUserProfile (staff/admin accounts intentionally excluded)
        public_user = PublicUserProfile.objects.filter(PUBLIC_USER_EMAIL__iexact=email).first()

        if public_user:
            try:
                uidb64 = urlsafe_base64_encode(force_bytes(public_user.pk))
                token = public_user_token_generator.make_token(public_user)
                reset_path = reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})
                reset_url = request.build_absolute_uri(reset_path)

                subject = "Reset your Holistic Nepal account password"
                message_text = (
                    f"Hello {public_user.PUBLIC_USER_FULL_NAME},\n\n"
                    f"We received a request to reset the password for your Holistic Nepal customer account.\n\n"
                    f"Click the link below to set a new password:\n{reset_url}\n\n"
                    f"This link is valid for 1 hour and can only be used once.\n"
                    f"If you did not make this request, you can safely ignore this email.\n\n"
                    f"Warm regards,\nHolistic Nepal Team"
                )
                from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'Holistic Nepal <noreply@holisticnepal.com>')
                send_mail(
                    subject,
                    message_text,
                    from_email,
                    [public_user.PUBLIC_USER_EMAIL],
                    fail_silently=False
                )
            except Exception as e:
                logger.error(f"Failed to send password reset email: {e}")

        # Always return success to prevent email enumeration attacks
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
            return JsonResponse({
                'status': 'success',
                'message': 'If an account exists with that email address, instructions have been sent.',
                'redirect_url': reverse('password_reset_done')
            })

        return redirect('password_reset_done')


class PasswordResetSentView(View):
    """
    Renders password reset instructions dispatched confirmation page.
    """
    def get(self, request):
        return render(request, 'auth/password_reset_done.html')


class PasswordResetConfirmView(View):
    """
    Validates token and handles new password submission for PublicUserProfile.
    """
    def _get_user(self, uidb64):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            return PublicUserProfile.objects.filter(pk=uid).first()
        except Exception:
            return None

    def get(self, request, uidb64, token):
        user = self._get_user(uidb64)
        validlink = bool(user and public_user_token_generator.check_token(user, token))
        return render(request, 'auth/password_reset_confirm.html', {
            'validlink': validlink,
            'uidb64': uidb64,
            'token': token,
        })

    def post(self, request, uidb64, token):
        user = self._get_user(uidb64)
        if not user or not public_user_token_generator.check_token(user, token):
            msg = "This password reset link is invalid or has expired."
            if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
                return JsonResponse({'status': 'error', 'message': msg}, status=400)
            return render(request, 'auth/password_reset_confirm.html', {'validlink': False})

        new_password = ''
        confirm_password = ''
        if request.content_type == 'application/json' or request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                data = json.loads(request.body.decode('utf-8')) if request.body else {}
                new_password = data.get('password', '')
                confirm_password = data.get('confirm_password', '')
            except Exception:
                pass
        if not new_password:
            new_password = request.POST.get('password', '')
            confirm_password = request.POST.get('confirm_password', '')

        if not new_password or len(new_password) < 6:
            err = "Password must be at least 6 characters long."
            if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
                return JsonResponse({'status': 'error', 'message': err}, status=400)
            return render(request, 'auth/password_reset_confirm.html', {
                'validlink': True,
                'uidb64': uidb64,
                'token': token,
                'error': err
            })

        if new_password != confirm_password:
            err = "Passwords do not match."
            if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
                return JsonResponse({'status': 'error', 'message': err}, status=400)
            return render(request, 'auth/password_reset_confirm.html', {
                'validlink': True,
                'uidb64': uidb64,
                'token': token,
                'error': err
            })

        # Update PublicUserProfile hashed password
        user.PUBLIC_USER_PASSWORD = make_password(new_password)
        user.save()

        # Also synchronize customer Django auth User if one exists
        try:
            django_user = User.objects.filter(email__iexact=user.PUBLIC_USER_EMAIL).first()
            if django_user:
                django_user.set_password(new_password)
                django_user.save()
        except Exception as e:
            logger.warning(f"Could not synchronize Django User password: {e}")

        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
            return JsonResponse({
                'status': 'success',
                'message': 'Password reset successful! Redirecting...',
                'redirect_url': reverse('password_reset_complete')
            })

        return redirect('password_reset_complete')


class PasswordResetCompleteView(View):
    """
    Renders password reset complete success page with login button.
    """
    def get(self, request):
        return render(request, 'auth/password_reset_complete.html')

