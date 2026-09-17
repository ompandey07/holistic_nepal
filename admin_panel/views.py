from .models import UnitSetup, ProductCategory, ProductSetup, ProductImage, ProductOrder, News, NewsImage, Gallery, GalleryImage
from django.db.models import Sum, Count, F, Q, DecimalField, ExpressionWrapper
from django.utils.decorators import method_decorator
from users.wrapper import advance_security_wrapper
from django.db.models.functions import TruncMonth
from django.core.paginator import Paginator
from users.models import EmployeeSetup
from django.http import JsonResponse
from django.core.cache import cache
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from django.views import View
import json


#?----------------------------------------------------------------------------------------------
#!- ADMIN DASHBOARD CLASS BASED VIEW PROTECTED WITH ADVANCE SECURITY WRAPPER
@method_decorator(advance_security_wrapper(allowed_roles=['ADMIN', 'CASHIER', 'DELIVERY_MAN', 'MANAGER', 'STAFF']), name='dispatch')
class AdminDashboardView(View):

    #!- CACHE TTL: 5 MINUTES - DASHBOARD AGGREGATIONS ARE EXPENSIVE, CACHE TO AVOID REPEATED DB HITS
    _CACHE_TTL = 300

    def _build_dashboard_stats(self):
        """
        COMPUTE ALL DASHBOARD AGGREGATIONS IN MINIMAL DB ROUND-TRIPS.
        CACHED FOR _CACHE_TTL SECONDS SO LAKH-SCALE DATA DOESN'T HAMMER THE DB ON EVERY REQUEST.
        """
        #!- REVENUE EXPRESSION: QTY X PRICE - REUSED ACROSS ALL REVENUE QUERIES
        revenue_expr = ExpressionWrapper(
            F('PRODUCT_ORDER_QTY') * F('PRODUCT_ORDER_PRODUCT__PRODUCT_PRICE'),
            output_field=DecimalField()
        )

        now = timezone.now()
        this_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        last_month_start = (this_month_start - timedelta(days=1)).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        six_months_ago   = now - timedelta(days=180)
        week_start = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)

        #!- SINGLE AGGREGATE QUERY: ALL ORDER-LEVEL STATS IN ONE DB ROUND-TRIP
        #!- USES Q() OBJECTS FOR CONDITIONAL COUNTS - F() CANNOT BE COMPARED TO PYTHON VALUES DIRECTLY
        order_agg = ProductOrder.objects.aggregate(
            total_orders      = Count('id'),
            pending_orders    = Count('id', filter=Q(PRODUCT_ORDER_STATUS='PENDING')),
            total_revenue     = Sum(revenue_expr),
            orders_this_month = Count('id', filter=Q(PRODUCT_ORDER_CREATED_AT__gte=this_month_start)),
            orders_last_month = Count('id', filter=Q(
                PRODUCT_ORDER_CREATED_AT__gte=last_month_start,
                PRODUCT_ORDER_CREATED_AT__lt=this_month_start
            )),
            revenue_this_month = Sum(revenue_expr, filter=Q(PRODUCT_ORDER_CREATED_AT__gte=this_month_start)),
            revenue_last_month = Sum(revenue_expr, filter=Q(
                PRODUCT_ORDER_CREATED_AT__gte=last_month_start,
                PRODUCT_ORDER_CREATED_AT__lt=this_month_start
            )),
        )

        #!- SAFELY EXTRACT VALUES WITH FALLBACK TO 0
        total_orders      = order_agg['total_orders']      or 0
        pending_orders    = order_agg['pending_orders']    or 0
        total_revenue     = order_agg['total_revenue']     or 0
        revenue_this_month = order_agg['revenue_this_month'] or 0
        revenue_last_month = order_agg['revenue_last_month'] or 0
        orders_this_month  = order_agg['orders_this_month']  or 0
        orders_last_month  = order_agg['orders_last_month']  or 0

        #!- PERCENTAGE DELTAS - SAFE DIVISION
        order_delta_pct   = round(((orders_this_month - orders_last_month) / orders_last_month) * 100, 1) if orders_last_month else 0
        revenue_delta_pct = round(((float(revenue_this_month) - float(revenue_last_month)) / float(revenue_last_month)) * 100, 1) if revenue_last_month else 0

        #!- SIMPLE COUNT QUERIES - EXTREMELY CHEAP (SINGLE SELECT COUNT)
        total_products   = ProductSetup.objects.count()
        total_employees  = EmployeeSetup.objects.count()
        total_categories = ProductCategory.objects.count()

        #!- MONTHLY REVENUE TREND - LAST 6 MONTHS (GROUPED AT DB LEVEL)
        monthly_revenue_qs = (
            ProductOrder.objects
            .filter(PRODUCT_ORDER_CREATED_AT__gte=six_months_ago)
            .annotate(month=TruncMonth('PRODUCT_ORDER_CREATED_AT'))
            .values('month')
            .annotate(revenue=Sum(revenue_expr))
            .order_by('month')
        )
        monthly_labels  = [row['month'].strftime('%b %Y') for row in monthly_revenue_qs]
        monthly_revenue = [float(row['revenue']) for row in monthly_revenue_qs]

        #!- ORDERS BY CATEGORY - THIS MONTH (TOP 6, DB-LEVEL GROUP-BY)
        category_qs = (
            ProductOrder.objects
            .filter(PRODUCT_ORDER_CREATED_AT__gte=this_month_start)
            .values('PRODUCT_ORDER_PRODUCT__PRODUCT_CATEGORY__CATEGORY_NAME')
            .annotate(cnt=Count('id'))
            .order_by('-cnt')[:6]
        )
        category_labels = [
            row['PRODUCT_ORDER_PRODUCT__PRODUCT_CATEGORY__CATEGORY_NAME'] or 'Uncategorised'
            for row in category_qs
        ]
        category_counts = [row['cnt'] for row in category_qs]

        #!- WEEKLY ORDERS - CURRENT WEEK (DJANGO WEEK_DAY: 1=SUNDAY ... 7=SATURDAY)
        DAY_NAMES    = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        daily_counts = [0] * 7
        dow_map      = {1: 6, 2: 0, 3: 1, 4: 2, 5: 3, 6: 4, 7: 5}
        weekly_qs = (
            ProductOrder.objects
            .filter(PRODUCT_ORDER_CREATED_AT__gte=week_start)
            .values('PRODUCT_ORDER_CREATED_AT__week_day')
            .annotate(cnt=Count('id'))
        )
        for row in weekly_qs:
            idx = dow_map.get(row['PRODUCT_ORDER_CREATED_AT__week_day'])
            if idx is not None:
                daily_counts[idx] = row['cnt']

        #!- RECENT 10 ORDERS - ONLY FETCH COLUMNS NEEDED FOR THE TABLE (AVOIDS LOADING HEAVY FIELDS)
        recent_orders = (
            ProductOrder.objects
            .select_related('PRODUCT_ORDER_PRODUCT', 'PRODUCT_ORDER_USER')
            .only(
                'PRODUCT_ORDER_ID',
                'PRODUCT_ORDER_QTY',
                'PRODUCT_ORDER_STATUS',
                'PRODUCT_ORDER_CREATED_AT',
                'PRODUCT_ORDER_USER__EMPLOYEE_FULL_NAME',
                'PRODUCT_ORDER_PRODUCT__PRODUCT_NAME',
                'PRODUCT_ORDER_PRODUCT__PRODUCT_PRICE',
            )
            .annotate(order_amount=ExpressionWrapper(
                F('PRODUCT_ORDER_QTY') * F('PRODUCT_ORDER_PRODUCT__PRODUCT_PRICE'),
                output_field=DecimalField()
            ))
            .order_by('-PRODUCT_ORDER_CREATED_AT')[:10]
        )

        return {
            #!- KPI CARDS
            'total_orders':       total_orders,
            'pending_orders':     pending_orders,
            'total_revenue':      total_revenue,
            'revenue_this_month': revenue_this_month,
            'order_delta_pct':    order_delta_pct,
            'revenue_delta_pct':  revenue_delta_pct,
            'total_products':     total_products,
            'total_employees':    total_employees,
            'total_categories':   total_categories,
            #!- CHARTS - SERIALISED TO JSON FOR INLINE JS
            'monthly_labels_json':  json.dumps(monthly_labels),
            'monthly_revenue_json': json.dumps(monthly_revenue),
            'category_labels_json': json.dumps(category_labels),
            'category_counts_json': json.dumps(category_counts),
            'weekly_labels_json':   json.dumps(DAY_NAMES),
            'weekly_orders_json':   json.dumps(daily_counts),
            #!- RECENT ORDERS TABLE
            'recent_orders': list(recent_orders),
        }

    def get(self, request):
        #!- TRY CACHE FIRST - AVOIDS RUNNING EXPENSIVE AGGREGATIONS ON EVERY PAGE LOAD
        cache_key = 'admin_dashboard_stats'
        context   = cache.get(cache_key)

        if context is None:
            #!- CACHE MISS - BUILD FROM DB AND STORE FOR _CACHE_TTL SECONDS
            context = self._build_dashboard_stats()
            cache.set(cache_key, context, timeout=self._CACHE_TTL)

        return render(request, 'admin/Dashboard/dashboard.html', context)



#?----------------------------------------------------------------------------------------------
#!- EMPLOYEE SETUP VIEW PROTECTED WITH ADVANCE SECURITY WRAPPER
@method_decorator(advance_security_wrapper(allowed_roles=['ADMIN', 'MANAGER']), name='dispatch')
class EmployeeSetupView(View):

    def get(self, request):
        #!- GET EMPLOYEE DATA WITH PAGINATION - ONLY COLUMNS NEEDED FOR THE TABLE
        page = request.GET.get('page', 1)
        employees = (
            EmployeeSetup.objects
            .only(
                'id',
                'EMPLOYEE_FULL_NAME',
                'EMPLOYEE_EMAIL',
                'EMPLOYEE_MOBILE_NO',
                'EMPLOYEE_ADDRESS',
                'EMPLOYEE_ROLE',
                'EMPLOYEE_CREATED_AT',
            )
            .order_by('-EMPLOYEE_CREATED_AT')
        )
        paginator      = Paginator(employees, 50)  #!- 50 RECORDS PER PAGE
        employees_page = paginator.get_page(page)

        context = {
            'employees':       employees_page,
            'total_employees': paginator.count,  #!- USES PAGINATOR CACHED COUNT - NO EXTRA QUERY
            'page_range':      paginator.get_elided_page_range(page, on_each_side=2, on_ends=1)
        }
        return render(request, 'admin/Employee/EmployeeSetup.html', context)

    def post(self, request):
        #!- ADD/UPDATE/DELETE EMPLOYEE WITH VALIDATION
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            action = request.POST.get('action', 'add')

            #!- HANDLE DELETE ACTION
            if action == 'delete':
                employee_id = request.POST.get('employee_id')
                if not employee_id:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Employee ID is required'
                    })

                try:
                    employee = EmployeeSetup.objects.get(id=employee_id)
                    employee.delete()
                    #!- INVALIDATE DASHBOARD CACHE SO EMPLOYEE COUNT REFRESHES
                    cache.delete('admin_dashboard_stats')
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Employee deleted successfully'
                    })
                except EmployeeSetup.DoesNotExist:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Employee not found'
                    })

            #!- HANDLE ADD/UPDATE ACTION
            employee_id = request.POST.get('employee_id', '').strip()
            full_name   = request.POST.get('full_name', '').strip()
            email       = request.POST.get('email', '').strip()
            mobile_no   = request.POST.get('mobile_no', '').strip()
            address     = request.POST.get('address', '').strip()
            role        = request.POST.get('role', 'STAFF')
            password    = request.POST.get('password', '').strip()

            errors = {}

            #!- VALIDATE FULL NAME
            if not full_name:
                errors['full_name'] = 'Full name is required'

            #!- VALIDATE EMAIL
            if not email:
                errors['email'] = 'Email is required'
            else:
                #!- CHECK FOR DUPLICATE EMAIL (EXCLUDE CURRENT EMPLOYEE FOR EDIT)
                email_query = EmployeeSetup.objects.filter(EMPLOYEE_EMAIL=email)
                if employee_id:
                    email_query = email_query.exclude(id=employee_id)
                if email_query.exists():
                    errors['email'] = 'Email already exists'

            #!- VALIDATE MOBILE NUMBER (MUST BE EXACTLY 10 DIGITS)
            if not mobile_no:
                errors['mobile_no'] = 'Mobile number is required'
            elif not mobile_no.isdigit() or len(mobile_no) != 10:
                errors['mobile_no'] = 'Mobile number must be exactly 10 digits'
            else:
                #!- CHECK FOR DUPLICATE MOBILE (EXCLUDE CURRENT EMPLOYEE FOR EDIT)
                mobile_query = EmployeeSetup.objects.filter(EMPLOYEE_MOBILE_NO=mobile_no)
                if employee_id:
                    mobile_query = mobile_query.exclude(id=employee_id)
                if mobile_query.exists():
                    errors['mobile_no'] = 'Mobile number already exists'

            #!- VALIDATE ADDRESS
            if not address:
                errors['address'] = 'Address is required'

            #!- VALIDATE PASSWORD (ONLY REQUIRED FOR NEW EMPLOYEES)
            if not employee_id and (not password or len(password) < 6):
                errors['password'] = 'Password must be at least 6 characters'

            if errors:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Please fix the highlighted fields',
                    'errors': errors
                })

            #!- GET CLIENT IP ADDRESS
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip_address = x_forwarded_for.split(',')[0].strip()
            else:
                ip_address = request.META.get('REMOTE_ADDR')

            #!- UPDATE EXISTING EMPLOYEE OR CREATE NEW ONE
            if employee_id:
                try:
                    employee = EmployeeSetup.objects.get(id=employee_id)
                    employee.EMPLOYEE_FULL_NAME  = full_name
                    employee.EMPLOYEE_EMAIL      = email
                    employee.EMPLOYEE_MOBILE_NO  = mobile_no
                    employee.EMPLOYEE_ADDRESS    = address
                    employee.EMPLOYEE_ROLE       = role
                    if password:
                        employee.EMPLOYEE_PASSWORD = password
                    employee.EMPLOYEE_MODIFIED_BY = request.session.get('employee_name', 'Admin')
                    employee.save(update_fields=[  #!- PARTIAL SAVE - ONLY TOUCH CHANGED COLUMNS
                        'EMPLOYEE_FULL_NAME', 'EMPLOYEE_EMAIL', 'EMPLOYEE_MOBILE_NO',
                        'EMPLOYEE_ADDRESS', 'EMPLOYEE_ROLE', 'EMPLOYEE_MODIFIED_BY',
                        *(['EMPLOYEE_PASSWORD'] if password else [])
                    ])

                    #!- INVALIDATE DASHBOARD CACHE ON DATA CHANGE
                    cache.delete('admin_dashboard_stats')
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Employee updated successfully',
                        'employee': {
                            'id':         employee.id,
                            'full_name':  employee.EMPLOYEE_FULL_NAME,
                            'email':      employee.EMPLOYEE_EMAIL,
                            'mobile_no':  employee.EMPLOYEE_MOBILE_NO,
                            'address':    employee.EMPLOYEE_ADDRESS,
                            'role':       employee.EMPLOYEE_ROLE,
                            'created_at': employee.EMPLOYEE_CREATED_AT.strftime('%Y-%m-%d %H:%M')
                        }
                    })
                except EmployeeSetup.DoesNotExist:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Employee not found'
                    })
            else:
                #!- CREATE NEW EMPLOYEE
                employee = EmployeeSetup.objects.create(
                    EMPLOYEE_FULL_NAME = full_name,
                    EMPLOYEE_EMAIL     = email,
                    EMPLOYEE_MOBILE_NO = mobile_no,
                    EMPLOYEE_ADDRESS   = address,
                    EMPLOYEE_IP        = ip_address,
                    EMPLOYEE_ROLE      = role,
                    EMPLOYEE_PASSWORD  = password,
                    EMPLOYEE_CREATED_BY = request.session.get('employee_name', 'Admin')
                )

                #!- INVALIDATE DASHBOARD CACHE SO EMPLOYEE COUNT REFRESHES
                cache.delete('admin_dashboard_stats')
                return JsonResponse({
                    'status': 'success',
                    'message': 'Employee added successfully',
                    'employee': {
                        'id':         employee.id,
                        'full_name':  employee.EMPLOYEE_FULL_NAME,
                        'email':      employee.EMPLOYEE_EMAIL,
                        'mobile_no':  employee.EMPLOYEE_MOBILE_NO,
                        'address':    employee.EMPLOYEE_ADDRESS,
                        'role':       employee.EMPLOYEE_ROLE,
                        'created_at': employee.EMPLOYEE_CREATED_AT.strftime('%Y-%m-%d %H:%M')
                    }
                })

        return JsonResponse({'status': 'error', 'message': 'Invalid request'})


#?----------------------------------------------------------------------------------------------
#!- UNIT SETUP VIEW PROTECTED WITH ADVANCE SECURITY WRAPPER
@method_decorator(advance_security_wrapper(allowed_roles=['ADMIN', 'MANAGER']), name='dispatch')
class UnitSetupView(View):

    def get(self, request):
        #!- FETCH ONLY REQUIRED COLUMNS - AVOIDS LOADING UNNECESSARY DATA FOR LARGE TABLES
        page  = request.GET.get('page', 1)
        units = (
            UnitSetup.objects
            .only('id', 'UNIT_NAME', 'UNIT_SYMBOL', 'UNIT_CREATED_AT')
            .order_by('-UNIT_CREATED_AT')
        )
        paginator  = Paginator(units, 50)
        units_page = paginator.get_page(page)

        context = {
            'units':       units_page,
            'total_units': paginator.count,  #!- PAGINATOR CACHED COUNT - NO EXTRA QUERY
            'page_range':  paginator.get_elided_page_range(page, on_each_side=2, on_ends=1)
        }
        return render(request, 'admin/Inventory/UnitSetup.html', context)

    def post(self, request):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            action = request.POST.get('action', 'add')

            if action == 'delete':
                unit_id = request.POST.get('unit_id')
                if not unit_id:
                    return JsonResponse({'status': 'error', 'message': 'Unit ID is required'})

                try:
                    unit = UnitSetup.objects.get(id=unit_id)
                    unit.delete()
                    return JsonResponse({'status': 'success', 'message': 'Unit deleted successfully'})
                except UnitSetup.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'Unit not found'})

            unit_id     = request.POST.get('unit_id', '').strip()
            unit_name   = request.POST.get('unit_name', '').strip()
            unit_symbol = request.POST.get('unit_symbol', '').strip()

            errors = {}

            if not unit_name:
                errors['unit_name'] = 'Unit name is required'
            else:
                name_query = UnitSetup.objects.filter(UNIT_NAME=unit_name)
                if unit_id:
                    name_query = name_query.exclude(id=unit_id)
                if name_query.exists():
                    errors['unit_name'] = 'Unit name already exists'

            if not unit_symbol:
                errors['unit_symbol'] = 'Unit symbol is required'
            else:
                symbol_query = UnitSetup.objects.filter(UNIT_SYMBOL=unit_symbol)
                if unit_id:
                    symbol_query = symbol_query.exclude(id=unit_id)
                if symbol_query.exists():
                    errors['unit_symbol'] = 'Unit symbol already exists'

            if errors:
                return JsonResponse({'status': 'error', 'message': 'Please fix the highlighted fields', 'errors': errors})

            #!- RESOLVE CREATED_BY EMPLOYEE FROM SESSION
            try:
                created_by = EmployeeSetup.objects.only('id').get(id=request.session.get('employee_id')) if request.session.get('employee_id') else None
            except Exception:
                created_by = None

            if unit_id:
                try:
                    unit = UnitSetup.objects.get(id=unit_id)
                    unit.UNIT_NAME        = unit_name
                    unit.UNIT_SYMBOL      = unit_symbol
                    unit.UNIT_MODIFIED_BY = created_by
                    unit.save(update_fields=['UNIT_NAME', 'UNIT_SYMBOL', 'UNIT_MODIFIED_BY'])  #!- PARTIAL SAVE
                    return JsonResponse({'status': 'success', 'message': 'Unit updated successfully'})
                except UnitSetup.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'Unit not found'})
            else:
                UnitSetup.objects.create(
                    UNIT_NAME       = unit_name,
                    UNIT_SYMBOL     = unit_symbol,
                    UNIT_CREATED_BY = created_by
                )
                return JsonResponse({'status': 'success', 'message': 'Unit added successfully'})

        return JsonResponse({'status': 'error', 'message': 'Invalid request'})


#?----------------------------------------------------------------------------------------------
#!- PRODUCT CATEGORY VIEW PROTECTED WITH ADVANCE SECURITY WRAPPER
@method_decorator(advance_security_wrapper(allowed_roles=['ADMIN', 'MANAGER']), name='dispatch')
class ProductCategoryView(View):

    def get(self, request):
        #!- FETCH ONLY REQUIRED COLUMNS FOR THE CATEGORY TABLE
        page       = request.GET.get('page', 1)
        categories = (
            ProductCategory.objects
            .only('id', 'CATEGORY_NAME', 'CATEGORY_IMAGE', 'CATEGORY_CREATED_AT')
            .order_by('-CATEGORY_CREATED_AT')
        )
        paginator       = Paginator(categories, 50)
        categories_page = paginator.get_page(page)

        context = {
            'categories':       categories_page,
            'total_categories': paginator.count,  #!- PAGINATOR CACHED COUNT - NO EXTRA QUERY
            'page_range':       paginator.get_elided_page_range(page, on_each_side=2, on_ends=1)
        }
        return render(request, 'admin/Inventory/ProductCategory.html', context)

    def post(self, request):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            action = request.POST.get('action', 'add')

            if action == 'delete':
                category_id = request.POST.get('category_id')
                if not category_id:
                    return JsonResponse({'status': 'error', 'message': 'Category ID is required'})

                try:
                    category = ProductCategory.objects.get(id=category_id)
                    category.delete()
                    #!- INVALIDATE DASHBOARD CACHE SO CATEGORY COUNT REFRESHES
                    cache.delete('admin_dashboard_stats')
                    return JsonResponse({'status': 'success', 'message': 'Category deleted successfully'})
                except ProductCategory.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'Category not found'})

            category_id    = request.POST.get('category_id', '').strip()
            category_name  = request.POST.get('category_name', '').strip()
            category_image = request.FILES.get('category_image')
            remove_image   = request.POST.get('remove_image') == 'true'

            errors = {}

            if not category_name:
                errors['category_name'] = 'Category name is required'
            else:
                name_query = ProductCategory.objects.filter(CATEGORY_NAME=category_name)
                if category_id:
                    name_query = name_query.exclude(id=category_id)
                if name_query.exists():
                    errors['category_name'] = 'Category name already exists'

            if errors:
                return JsonResponse({'status': 'error', 'message': 'Please fix the highlighted fields', 'errors': errors})

            #!- RESOLVE CREATED_BY EMPLOYEE FROM SESSION
            try:
                created_by = EmployeeSetup.objects.only('id').get(id=request.session.get('employee_id')) if request.session.get('employee_id') else None
            except Exception:
                created_by = None

            if category_id:
                try:
                    category = ProductCategory.objects.get(id=category_id)
                    category.CATEGORY_NAME        = category_name
                    category.CATEGORY_MODIFIED_BY = created_by
                    update_fields = ['CATEGORY_NAME', 'CATEGORY_MODIFIED_BY']
                    if remove_image:
                        category.CATEGORY_IMAGE = None
                        update_fields.append('CATEGORY_IMAGE')
                    elif category_image:
                        category.CATEGORY_IMAGE = category_image
                        update_fields.append('CATEGORY_IMAGE')
                    category.save(update_fields=update_fields)  #!- PARTIAL SAVE
                    return JsonResponse({'status': 'success', 'message': 'Category updated successfully'})
                except ProductCategory.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'Category not found'})
            else:
                ProductCategory.objects.create(
                    CATEGORY_NAME       = category_name,
                    CATEGORY_IMAGE      = category_image if not remove_image else None,
                    CATEGORY_CREATED_BY = created_by
                )
                #!- INVALIDATE DASHBOARD CACHE SO CATEGORY COUNT REFRESHES
                cache.delete('admin_dashboard_stats')
                return JsonResponse({'status': 'success', 'message': 'Category added successfully'})

        return JsonResponse({'status': 'error', 'message': 'Invalid request'})



#?----------------------------------------------------------------------------------------------
#!- PRODUCT SETUP VIEW PROTECTED WITH ADVANCE SECURITY WRAPPER
@method_decorator(advance_security_wrapper(allowed_roles=['ADMIN', 'MANAGER']), name='dispatch')
class ProductSetupView(View):

    def get(self, request):
        #!- FETCH ONLY REQUIRED COLUMNS FOR PRODUCT LIST - DEFERS HEAVY DESCRIPTION/IMAGE FIELDS
        page     = request.GET.get('page', 1)
        products = (
            ProductSetup.objects
            .select_related('PRODUCT_UNIT', 'PRODUCT_CATEGORY')
            .prefetch_related('PRODUCT_IMAGES')
            .only(
                'id',
                'PRODUCT_NAME',
                'PRODUCT_SLUG',
                'PRODUCT_PRICE',
                'PRODUCT_SIZE',
                'PRODUCT_WEIGHT',
                'PRODUCT_DESCRIPTION',
                'PRODUCT_KEY_FEATURES',
                'PRODUCT_IMAGE',
                'PRODUCT_CREATED_AT',
                'PRODUCT_UNIT__UNIT_NAME',
                'PRODUCT_UNIT__UNIT_SYMBOL',
                'PRODUCT_CATEGORY__CATEGORY_NAME',
            )
            .order_by('-PRODUCT_CREATED_AT')
        )
        paginator     = Paginator(products, 50)
        products_page = paginator.get_page(page)

        #!- UNITS AND CATEGORIES FOR DROPDOWNS - CACHED TO AVOID REPEATED QUERIES ON PAGE REFRESH
        units_cache_key      = 'product_setup_units'
        categories_cache_key = 'product_setup_categories'

        units = cache.get(units_cache_key)
        if units is None:
            units = list(UnitSetup.objects.only('id', 'UNIT_NAME', 'UNIT_SYMBOL'))
            cache.set(units_cache_key, units, timeout=600)  #!- CACHE DROPDOWNS FOR 10 MINUTES

        categories = cache.get(categories_cache_key)
        if categories is None:
            categories = list(ProductCategory.objects.only('id', 'CATEGORY_NAME'))
            cache.set(categories_cache_key, categories, timeout=600)

        context = {
            'products':       products_page,
            'total_products': paginator.count,  #!- PAGINATOR CACHED COUNT - NO EXTRA QUERY
            'units':          units,
            'categories':     categories,
            'page_range':     paginator.get_elided_page_range(page, on_each_side=2, on_ends=1)
        }
        return render(request, 'admin/Inventory/ProductSetup.html', context)

    def post(self, request):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            action = request.POST.get('action', 'add')

            if action == 'delete':
                product_id = request.POST.get('product_id')
                if not product_id:
                    return JsonResponse({'status': 'error', 'message': 'Product ID is required'})

                try:
                    product = ProductSetup.objects.get(id=product_id)
                    product.delete()
                    #!- INVALIDATE DASHBOARD AND PRODUCT DROPDOWN CACHES
                    cache.delete_many(['admin_dashboard_stats', 'product_setup_units', 'product_setup_categories'])
                    return JsonResponse({'status': 'success', 'message': 'Product deleted successfully'})
                except ProductSetup.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'Product not found'})

            if action == 'delete_single_image':
                image_id = request.POST.get('image_id')
                if not image_id:
                    return JsonResponse({'status': 'error', 'message': 'Image ID is required'})
                try:
                    img = ProductImage.objects.get(id=image_id)
                    product = img.PRODUCT
                    img.delete()
                    if product.PRODUCT_IMAGE and img.IMAGE and product.PRODUCT_IMAGE.name == img.IMAGE.name:
                        next_img = product.PRODUCT_IMAGES.first()
                        product.PRODUCT_IMAGE = next_img.IMAGE if next_img else None
                        product.save(update_fields=['PRODUCT_IMAGE'])
                    return JsonResponse({'status': 'success', 'message': 'Image deleted successfully'})
                except ProductImage.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'Image not found'})

            product_id           = request.POST.get('product_id', '').strip()
            product_name         = request.POST.get('product_name', '').strip()
            product_unit         = request.POST.get('product_unit', '').strip()
            product_category     = request.POST.get('product_category', '').strip()
            product_price        = request.POST.get('product_price', '').strip()
            product_size         = request.POST.get('product_size', '').strip()
            product_weight       = request.POST.get('product_weight', '').strip()
            product_description  = request.POST.get('product_description', '').strip()
            product_key_features = request.POST.get('product_key_features', '').strip()
            deleted_image_ids    = request.POST.get('deleted_image_ids', '').strip()

            #!- MULTIPLE IMAGES UPLOAD HANDLER
            uploaded_images = request.FILES.getlist('product_images')
            if not uploaded_images and request.FILES.get('product_image'):
                uploaded_images = [request.FILES.get('product_image')]

            errors = {}

            if not product_name:
                errors['product_name'] = 'Product name is required'

            if not product_unit:
                errors['product_unit'] = 'Unit is required'

            if not product_category:
                errors['product_category'] = 'Category is required'

            if not product_price:
                errors['product_price'] = 'Price is required'
            else:
                try:
                    price_val = float(product_price)
                    if price_val <= 0:
                        errors['product_price'] = 'Price must be greater than 0'
                except ValueError:
                    errors['product_price'] = 'Price must be a valid number'

            if not product_description:
                errors['product_description'] = 'Description is required'

            if errors:
                return JsonResponse({'status': 'error', 'message': 'Please fix the highlighted fields', 'errors': errors})

            try:
                created_by = EmployeeSetup.objects.only('id').get(id=request.session.get('employee_id')) if request.session.get('employee_id') else None
                unit       = UnitSetup.objects.only('id').get(id=product_unit)
                category   = ProductCategory.objects.only('id').get(id=product_category)
            except UnitSetup.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Invalid unit selected'})
            except ProductCategory.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Invalid category selected'})
            except Exception:
                created_by = None

            if product_id:
                try:
                    product = ProductSetup.objects.get(id=product_id)
                    product.PRODUCT_NAME         = product_name
                    product.PRODUCT_UNIT         = unit
                    product.PRODUCT_CATEGORY     = category
                    product.PRODUCT_PRICE        = product_price
                    product.PRODUCT_SIZE         = product_size
                    product.PRODUCT_WEIGHT       = product_weight
                    product.PRODUCT_DESCRIPTION  = product_description
                    product.PRODUCT_KEY_FEATURES = product_key_features
                    product.PRODUCT_MODIFIED_BY  = created_by

                    #!- PROCESS DELETED EXISTING IMAGES IF ANY
                    if deleted_image_ids:
                        del_ids = [int(i.strip()) for i in deleted_image_ids.split(',') if i.strip().isdigit()]
                        if del_ids:
                            ProductImage.objects.filter(id__in=del_ids, PRODUCT=product).delete()

                    #!- SAVE NEW MULTIPLE IMAGES FIRST
                    for img_file in uploaded_images:
                        ProductImage.objects.create(PRODUCT=product, IMAGE=img_file)

                    #!- UPDATE MAIN COVER IMAGE FROM SAVED GALLERY IMAGES IF NEEDED
                    first_gallery_img = product.PRODUCT_IMAGES.first()
                    if first_gallery_img and (not product.PRODUCT_IMAGE or not product.PRODUCT_IMAGE.name):
                        product.PRODUCT_IMAGE = first_gallery_img.IMAGE

                    product.save()
                    #!- INVALIDATE DASHBOARD CACHE ON PRODUCT CHANGE
                    cache.delete('admin_dashboard_stats')
                    return JsonResponse({'status': 'success', 'message': 'Product updated successfully'})
                except ProductSetup.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'Product not found'})
            else:
                product = ProductSetup.objects.create(
                    PRODUCT_NAME         = product_name,
                    PRODUCT_UNIT         = unit,
                    PRODUCT_CATEGORY     = category,
                    PRODUCT_PRICE        = product_price,
                    PRODUCT_SIZE         = product_size,
                    PRODUCT_WEIGHT       = product_weight,
                    PRODUCT_DESCRIPTION  = product_description,
                    PRODUCT_KEY_FEATURES = product_key_features,
                    PRODUCT_IMAGE        = None,
                    PRODUCT_CREATED_BY   = created_by
                )
                #!- SAVE ALL MULTIPLE IMAGES FOR NEW PRODUCT
                for img_file in uploaded_images:
                    ProductImage.objects.create(PRODUCT=product, IMAGE=img_file)

                first_gallery_img = product.PRODUCT_IMAGES.first()
                if first_gallery_img:
                    product.PRODUCT_IMAGE = first_gallery_img.IMAGE
                    product.save(update_fields=['PRODUCT_IMAGE'])

                #!- INVALIDATE DASHBOARD CACHE SO PRODUCT COUNT REFRESHES
                cache.delete('admin_dashboard_stats')
                return JsonResponse({'status': 'success', 'message': 'Product added successfully'})

        return JsonResponse({'status': 'error', 'message': 'Invalid request'})


#?----------------------------------------------------------------------------------------------
#!- NEWS SETUP VIEW PROTECTED WITH ADVANCE SECURITY WRAPPER
@method_decorator(advance_security_wrapper(allowed_roles=['ADMIN', 'MANAGER']), name='dispatch')
class NewsSetupView(View):

    def get(self, request):
        page = request.GET.get('page', 1)
        news_qs = (
            News.objects
            .select_related('NEWS_CREATED_BY')
            .prefetch_related('NEWS_IMAGES')
            .order_by('-NEWS_CREATED_AT')
        )
        paginator = Paginator(news_qs, 50)
        news_page = paginator.get_page(page)

        news_types = News._meta.get_field('NEWS_TYPE').choices

        context = {
            'news_list':  news_page,
            'total_news': paginator.count,
            'news_types': news_types,
            'page_range': paginator.get_elided_page_range(page, on_each_side=2, on_ends=1)
        }
        return render(request, 'admin/News/NewsSetup.html', context)

    def post(self, request):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            action = request.POST.get('action', 'add')

            if action == 'delete':
                news_id = request.POST.get('news_id')
                if not news_id:
                    return JsonResponse({'status': 'error', 'message': 'News ID is required'})

                try:
                    news_item = News.objects.get(id=news_id)
                    news_item.delete()
                    return JsonResponse({'status': 'success', 'message': 'News deleted successfully'})
                except News.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'News not found'})

            if action == 'delete_single_image':
                image_id = request.POST.get('image_id')
                if not image_id:
                    return JsonResponse({'status': 'error', 'message': 'Image ID is required'})
                try:
                    img = NewsImage.objects.get(id=image_id)
                    news_item = img.NEWS
                    img.delete()
                    if news_item.NEWS_IMAGE and img.IMAGE and news_item.NEWS_IMAGE.name == img.IMAGE.name:
                        next_img = news_item.NEWS_IMAGES.first()
                        news_item.NEWS_IMAGE = next_img.IMAGE if next_img else None
                        news_item.save(update_fields=['NEWS_IMAGE'])
                    return JsonResponse({'status': 'success', 'message': 'Image deleted successfully'})
                except NewsImage.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'Image not found'})

            news_id           = request.POST.get('news_id', '').strip()
            news_type         = request.POST.get('news_type', '').strip()
            news_title        = request.POST.get('news_title', '').strip()
            news_description  = request.POST.get('news_description', '').strip()
            deleted_image_ids = request.POST.get('deleted_image_ids', '').strip()

            uploaded_images = request.FILES.getlist('news_images')
            if not uploaded_images and request.FILES.get('news_image'):
                uploaded_images = [request.FILES.get('news_image')]

            errors = {}

            if not news_type:
                errors['news_type'] = 'News type is required'

            if not news_title:
                errors['news_title'] = 'News title is required'

            if not news_description:
                errors['news_description'] = 'News description is required'

            if errors:
                return JsonResponse({'status': 'error', 'message': 'Please fix the highlighted fields', 'errors': errors})

            try:
                created_by = EmployeeSetup.objects.only('id').get(id=request.session.get('employee_id')) if request.session.get('employee_id') else None
            except Exception:
                created_by = None

            if news_id:
                try:
                    news_item = News.objects.get(id=news_id)
                    news_item.NEWS_TYPE        = news_type
                    news_item.NEWS_TITLE       = news_title
                    news_item.NEWS_DESCRIPTION = news_description
                    news_item.NEWS_MODIFIED_BY = created_by

                    if deleted_image_ids:
                        del_ids = [int(i.strip()) for i in deleted_image_ids.split(',') if i.strip().isdigit()]
                        if del_ids:
                            NewsImage.objects.filter(id__in=del_ids, NEWS=news_item).delete()

                    for img_file in uploaded_images:
                        NewsImage.objects.create(NEWS=news_item, IMAGE=img_file)

                    first_gallery_img = news_item.NEWS_IMAGES.first()
                    if first_gallery_img and (not news_item.NEWS_IMAGE or not news_item.NEWS_IMAGE.name):
                        news_item.NEWS_IMAGE = first_gallery_img.IMAGE

                    news_item.save()
                    return JsonResponse({'status': 'success', 'message': 'News updated successfully'})
                except News.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'News not found'})
            else:
                news_item = News.objects.create(
                    NEWS_TYPE        = news_type,
                    NEWS_TITLE       = news_title,
                    NEWS_DESCRIPTION = news_description,
                    NEWS_IMAGE       = None,
                    NEWS_CREATED_BY  = created_by
                )
                for img_file in uploaded_images:
                    NewsImage.objects.create(NEWS=news_item, IMAGE=img_file)

                first_gallery_img = news_item.NEWS_IMAGES.first()
                if first_gallery_img:
                    news_item.NEWS_IMAGE = first_gallery_img.IMAGE
                    news_item.save(update_fields=['NEWS_IMAGE'])

                return JsonResponse({'status': 'success', 'message': 'News added successfully'})

        return JsonResponse({'status': 'error', 'message': 'Invalid request'})


#?----------------------------------------------------------------------------------------------
#!- GALLERY SETUP VIEW PROTECTED WITH ADVANCE SECURITY WRAPPER
@method_decorator(advance_security_wrapper(allowed_roles=['ADMIN', 'MANAGER']), name='dispatch')
class GallerySetupView(View):

    def get(self, request):
        page = request.GET.get('page', 1)
        gallery_qs = (
            Gallery.objects
            .select_related('GALLERY_CREATED_BY')
            .prefetch_related('GALLERY_IMAGES')
            .order_by('-GALLERY_CREATED_AT')
        )
        paginator = Paginator(gallery_qs, 50)
        gallery_page = paginator.get_page(page)

        context = {
            'gallery_list':  gallery_page,
            'total_gallery': paginator.count,
            'page_range':    paginator.get_elided_page_range(page, on_each_side=2, on_ends=1)
        }
        return render(request, 'admin/Gallery/GallerySetup.html', context)

    def post(self, request):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            action = request.POST.get('action', 'add')

            if action == 'delete':
                gallery_id = request.POST.get('gallery_id')
                if not gallery_id:
                    return JsonResponse({'status': 'error', 'message': 'Gallery ID is required'})

                try:
                    gallery_item = Gallery.objects.get(id=gallery_id)
                    gallery_item.delete()
                    return JsonResponse({'status': 'success', 'message': 'Gallery deleted successfully'})
                except Gallery.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'Gallery item not found'})

            if action == 'delete_single_image':
                image_id = request.POST.get('image_id')
                if not image_id:
                    return JsonResponse({'status': 'error', 'message': 'Image ID is required'})
                try:
                    img = GalleryImage.objects.get(id=image_id)
                    gallery_item = img.GALLERY
                    img.delete()
                    if gallery_item.GALLERY_IMAGE and img.IMAGE and gallery_item.GALLERY_IMAGE.name == img.IMAGE.name:
                        next_img = gallery_item.GALLERY_IMAGES.first()
                        gallery_item.GALLERY_IMAGE = next_img.IMAGE if next_img else None
                        gallery_item.save(update_fields=['GALLERY_IMAGE'])
                    return JsonResponse({'status': 'success', 'message': 'Image deleted successfully'})
                except GalleryImage.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'Image not found'})

            gallery_id          = request.POST.get('gallery_id', '').strip()
            gallery_title       = request.POST.get('gallery_title', '').strip()
            gallery_description = request.POST.get('gallery_description', '').strip()
            deleted_image_ids   = request.POST.get('deleted_image_ids', '').strip()

            uploaded_images = request.FILES.getlist('gallery_images')
            if not uploaded_images and request.FILES.get('gallery_image'):
                uploaded_images = [request.FILES.get('gallery_image')]

            errors = {}

            if not gallery_title:
                errors['gallery_title'] = 'Gallery title is required'

            if not gallery_description:
                errors['gallery_description'] = 'Gallery description is required'

            if errors:
                return JsonResponse({'status': 'error', 'message': 'Please fix the highlighted fields', 'errors': errors})

            try:
                created_by = EmployeeSetup.objects.only('id').get(id=request.session.get('employee_id')) if request.session.get('employee_id') else None
            except Exception:
                created_by = None

            if gallery_id:
                try:
                    gallery_item = Gallery.objects.get(id=gallery_id)
                    gallery_item.GALLERY_TITLE       = gallery_title
                    gallery_item.GALLERY_DESCRIPTION = gallery_description
                    gallery_item.GALLERY_MODIFIED_BY = created_by

                    if deleted_image_ids:
                        del_ids = [int(i.strip()) for i in deleted_image_ids.split(',') if i.strip().isdigit()]
                        if del_ids:
                            GalleryImage.objects.filter(id__in=del_ids, GALLERY=gallery_item).delete()

                    for img_file in uploaded_images:
                        GalleryImage.objects.create(GALLERY=gallery_item, IMAGE=img_file)

                    first_gallery_img = gallery_item.GALLERY_IMAGES.first()
                    if first_gallery_img and (not gallery_item.GALLERY_IMAGE or not gallery_item.GALLERY_IMAGE.name):
                        gallery_item.GALLERY_IMAGE = first_gallery_img.IMAGE

                    gallery_item.save()
                    return JsonResponse({'status': 'success', 'message': 'Gallery updated successfully'})
                except Gallery.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'Gallery not found'})
            else:
                gallery_item = Gallery.objects.create(
                    GALLERY_TITLE       = gallery_title,
                    GALLERY_DESCRIPTION = gallery_description,
                    GALLERY_IMAGE       = None,
                    GALLERY_CREATED_BY  = created_by
                )
                for img_file in uploaded_images:
                    GalleryImage.objects.create(GALLERY=gallery_item, IMAGE=img_file)

                first_gallery_img = gallery_item.GALLERY_IMAGES.first()
                if first_gallery_img:
                    gallery_item.GALLERY_IMAGE = first_gallery_img.IMAGE
                    gallery_item.save(update_fields=['GALLERY_IMAGE'])

                return JsonResponse({'status': 'success', 'message': 'Gallery added successfully'})

        return JsonResponse({'status': 'error', 'message': 'Invalid request'})


