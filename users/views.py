from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.core.cache import cache
from users.models import PublicUserProfile
from admin_panel.models import ProductSetup, ProductOrder
from django.db.models import Sum, F, Q, ExpressionWrapper, DecimalField, Count
from django.utils import timezone
import json


#!- USER DASHBOARD VIEW - PROTECTED WITH LOGIN REQUIRED
@method_decorator(login_required, name='dispatch')
class UserDashboardView(View):

    def get(self, request):
        #!- GET USER PROFILE DATA
        try:
            user_profile = PublicUserProfile.objects.get(
                PUBLIC_USER_EMAIL=request.user.email
            )
        except PublicUserProfile.DoesNotExist:
            user_profile = None

        #!- REAL CUSTOMER ORDERS QUERY
        if user_profile:
            orders_qs = ProductOrder.objects.filter(CUSTOMER=user_profile).select_related('PRODUCT_ORDER_PRODUCT').order_by('-PRODUCT_ORDER_CREATED_AT')
        else:
            orders_qs = ProductOrder.objects.none()

        page = request.GET.get('page', 1)
        paginator = Paginator(orders_qs, 10)
        orders_page = paginator.get_page(page)

        total_orders = orders_qs.count()
        total_spent = sum([float(o.order_amount) for o in orders_qs])
        pending_orders = orders_qs.filter(PRODUCT_ORDER_STATUS='PENDING').count()
        completed_orders = orders_qs.filter(PRODUCT_ORDER_STATUS__in=['DELIVERED', 'CONFIRMED']).count()

        order_stats = {
            'total_orders': total_orders,
            'total_spent': total_spent,
            'pending_orders': pending_orders,
            'completed_orders': completed_orders
        }

        context = {
            'user_profile': user_profile,
            'orders': orders_page,
            'total_orders': total_orders,
            'page_range': paginator.get_elided_page_range(orders_page.number, on_each_side=1, on_ends=1) if total_orders > 0 else [],
            'order_stats': order_stats,
        }
        return render(request, 'users/Dashboard/dashboard.html', context)


#!- USER ORDERS VIEW - PROTECTED WITH LOGIN REQUIRED
@method_decorator(login_required, name='dispatch')
class UserOrdersView(View):

    def get(self, request):
        #!- GET USER PROFILE DATA
        try:
            user_profile = PublicUserProfile.objects.get(
                PUBLIC_USER_EMAIL=request.user.email
            )
        except PublicUserProfile.DoesNotExist:
            user_profile = None

        page = request.GET.get('page', 1)
        status_filter = request.GET.get('status', '').strip().upper()

        if user_profile:
            orders_qs = ProductOrder.objects.filter(CUSTOMER=user_profile).select_related('PRODUCT_ORDER_PRODUCT').order_by('-PRODUCT_ORDER_CREATED_AT')
        else:
            orders_qs = ProductOrder.objects.none()

        if status_filter:
            orders_qs = orders_qs.filter(PRODUCT_ORDER_STATUS=status_filter)

        total_orders = orders_qs.count()
        paginator = Paginator(orders_qs, 20)
        orders_page = paginator.get_page(page)

        context = {
            'user_profile': user_profile,
            'orders': orders_page,
            'total_orders': total_orders,
            'page_range': paginator.get_elided_page_range(orders_page.number, on_each_side=1, on_ends=1) if total_orders > 0 else [],
            'status_filter': status_filter,
        }
        return render(request, 'users/Orders/orders.html', context)


#!- USER SETTINGS VIEW - PROTECTED WITH LOGIN REQUIRED
@method_decorator(login_required, name='dispatch')
class UserSettingsView(View):

    def get(self, request):
        #!- GET USER PROFILE DATA
        try:
            user_profile = PublicUserProfile.objects.get(
                PUBLIC_USER_EMAIL=request.user.email
            )
        except PublicUserProfile.DoesNotExist:
            user_profile = None

        context = {
            'user_profile': user_profile,
        }
        return render(request, 'users/Settings/settings.html', context)

    def post(self, request):
        #!- UPDATE USER PROFILE SETTINGS
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            action = request.POST.get('action', 'profile')
            
            #!- HANDLE PASSWORD CHANGE
            if action == 'password':
                current_password = request.POST.get('current_password', '').strip()
                new_password = request.POST.get('new_password', '').strip()
                confirm_password = request.POST.get('confirm_password', '').strip()
                
                errors = {}
                
                if not current_password:
                    errors['current_password'] = 'Current password is required'
                elif not request.user.check_password(current_password):
                    errors['current_password'] = 'Current password is incorrect'
                
                if not new_password:
                    errors['new_password'] = 'New password is required'
                elif len(new_password) < 6:
                    errors['new_password'] = 'Password must be at least 6 characters'
                
                if not confirm_password:
                    errors['confirm_password'] = 'Please confirm your new password'
                elif new_password and confirm_password and new_password != confirm_password:
                    errors['confirm_password'] = 'Passwords do not match'
                
                if errors:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Please fix the highlighted fields',
                        'errors': errors
                    })
                
                #!- UPDATE PASSWORD IN DJANGO USER
                request.user.set_password(new_password)
                request.user.save()
                
                #!- UPDATE PASSWORD IN PUBLIC USER PROFILE IF EXISTS
                try:
                    user_profile = PublicUserProfile.objects.get(
                        PUBLIC_USER_EMAIL=request.user.email
                    )
                    from django.contrib.auth.hashers import make_password
                    user_profile.PUBLIC_USER_PASSWORD = make_password(new_password)
                    user_profile.save()
                except PublicUserProfile.DoesNotExist:
                    pass
                
                return JsonResponse({
                    'status': 'success',
                    'message': 'Password updated successfully'
                })
            
            #!- HANDLE PROFILE UPDATE
            full_name = request.POST.get('full_name', '').strip()
            mobile_no = request.POST.get('mobile_no', '').strip()
            address = request.POST.get('address', '').strip()
            profile_image = request.FILES.get('profile_image')

            errors = {}

            if not full_name:
                errors['full_name'] = 'Full name is required'

            if not mobile_no:
                errors['mobile_no'] = 'Mobile number is required'
            elif not mobile_no.isdigit() or len(mobile_no) != 10:
                errors['mobile_no'] = 'Mobile number must be exactly 10 digits'

            if not address:
                errors['address'] = 'Address is required'

            if errors:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Please fix the highlighted fields',
                    'errors': errors
                })

            #!- GET OR CREATE USER PROFILE
            try:
                user_profile = PublicUserProfile.objects.get(
                    PUBLIC_USER_EMAIL=request.user.email
                )
            except PublicUserProfile.DoesNotExist:
                user_profile = PublicUserProfile.objects.create(
                    PUBLIC_USER_EMAIL=request.user.email,
                    PUBLIC_USER_PASSWORD=request.user.password,  # In production, handle this properly
                )

            #!- UPDATE USER PROFILE
            user_profile.PUBLIC_USER_FULL_NAME = full_name
            user_profile.PUBLIC_USER_MOBILE_NO = mobile_no
            user_profile.PUBLIC_USER_ADDRESS = address
            if profile_image:
                user_profile.PUBLIC_USER_PROFILE_IMAGE = profile_image
            user_profile.PUBLIC_USER_MODIFIED_BY = full_name
            user_profile.save()

            return JsonResponse({
                'status': 'success',
                'message': 'Profile updated successfully'
            })

        return JsonResponse({'status': 'error', 'message': 'Invalid request'})
