from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.urls import reverse
import json

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
