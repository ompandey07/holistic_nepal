from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.http import JsonResponse
from users.wrapper import advance_security_wrapper
from users.models import EmployeeSetup
from .models import UnitSetup, ProductCategory, ProductSetup


#!- ADMIN DASHBOARD CLASS BASED VIEW PROTECTED WITH ADVANCE SECURITY WRAPPER
@method_decorator(advance_security_wrapper(allowed_roles=['ADMIN', 'CASHIER', 'DELIVERY_MAN', 'MANAGER', 'STAFF']), name='dispatch')
class AdminDashboardView(View):

    def get(self, request):
        #!- RENDER ADMIN DASHBOARD HTML TEMPLATE FOR AUTHORIZED EMPLOYEES AND SUPERUSERS
        return render(request, 'admin/Dashboard/dashboard.html')


#!- EMPLOYEE SETUP VIEW PROTECTED WITH ADVANCE SECURITY WRAPPER
@method_decorator(advance_security_wrapper(allowed_roles=['ADMIN', 'MANAGER']), name='dispatch')
class EmployeeSetupView(View):

    def get(self, request):
        #!- GET EMPLOYEE DATA WITH PAGINATION
        page = request.GET.get('page', 1)
        employees = EmployeeSetup.objects.all().order_by('-EMPLOYEE_CREATED_AT')
        paginator = Paginator(employees, 50)  # 50 records per page
        employees_page = paginator.get_page(page)
        
        context = {
            'employees': employees_page,
            'total_employees': employees.count(),
            'page_range': paginator.get_elided_page_range(page, on_each_side=2, on_ends=1)
        }
        return render(request, 'admin/Employee/EmployeeSetup.html', context)

    def post(self, request):
        #!- ADD/UPDATE/DELETE EMPLOYEE WITH VALIDATION
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            action = request.POST.get('action', 'add')
            
            # Handle DELETE action
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
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Employee deleted successfully'
                    })
                except EmployeeSetup.DoesNotExist:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Employee not found'
                    })
            
            # Handle ADD/UPDATE action
            employee_id = request.POST.get('employee_id', '').strip()
            full_name = request.POST.get('full_name', '').strip()
            email = request.POST.get('email', '').strip()
            mobile_no = request.POST.get('mobile_no', '').strip()
            address = request.POST.get('address', '').strip()
            role = request.POST.get('role', 'STAFF')
            password = request.POST.get('password', '').strip()
            
            errors = {}
            
            # Validate full name
            if not full_name:
                errors['full_name'] = 'Full name is required'
            
            # Validate email
            if not email:
                errors['email'] = 'Email is required'
            else:
                # Check for duplicate email (exclude current employee for edit)
                email_query = EmployeeSetup.objects.filter(EMPLOYEE_EMAIL=email)
                if employee_id:
                    email_query = email_query.exclude(id=employee_id)
                if email_query.exists():
                    errors['email'] = 'Email already exists'
            
            # Validate mobile number (must be exactly 10 digits)
            if not mobile_no:
                errors['mobile_no'] = 'Mobile number is required'
            elif not mobile_no.isdigit() or len(mobile_no) != 10:
                errors['mobile_no'] = 'Mobile number must be exactly 10 digits'
            else:
                # Check for duplicate mobile (exclude current employee for edit)
                mobile_query = EmployeeSetup.objects.filter(EMPLOYEE_MOBILE_NO=mobile_no)
                if employee_id:
                    mobile_query = mobile_query.exclude(id=employee_id)
                if mobile_query.exists():
                    errors['mobile_no'] = 'Mobile number already exists'
            
            # Validate address
            if not address:
                errors['address'] = 'Address is required'
            
            # Validate password (only required for new employees)
            if not employee_id and (not password or len(password) < 6):
                errors['password'] = 'Password must be at least 6 characters'
            
            if errors:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Please fix the highlighted fields',
                    'errors': errors
                })
            
            # Get client IP
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip_address = x_forwarded_for.split(',')[0]
            else:
                ip_address = request.META.get('REMOTE_ADDR')
            
            # Update existing employee or create new one
            if employee_id:
                try:
                    employee = EmployeeSetup.objects.get(id=employee_id)
                    employee.EMPLOYEE_FULL_NAME = full_name
                    employee.EMPLOYEE_EMAIL = email
                    employee.EMPLOYEE_MOBILE_NO = mobile_no
                    employee.EMPLOYEE_ADDRESS = address
                    employee.EMPLOYEE_ROLE = role
                    if password:
                        employee.EMPLOYEE_PASSWORD = password
                    employee.EMPLOYEE_MODIFIED_BY = request.session.get('employee_name', 'Admin')
                    employee.save()
                    
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Employee updated successfully',
                        'employee': {
                            'id': employee.id,
                            'full_name': employee.EMPLOYEE_FULL_NAME,
                            'email': employee.EMPLOYEE_EMAIL,
                            'mobile_no': employee.EMPLOYEE_MOBILE_NO,
                            'address': employee.EMPLOYEE_ADDRESS,
                            'role': employee.EMPLOYEE_ROLE,
                            'created_at': employee.EMPLOYEE_CREATED_AT.strftime('%Y-%m-%d %H:%M')
                        }
                    })
                except EmployeeSetup.DoesNotExist:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Employee not found'
                    })
            else:
                # Create new employee
                employee = EmployeeSetup.objects.create(
                    EMPLOYEE_FULL_NAME=full_name,
                    EMPLOYEE_EMAIL=email,
                    EMPLOYEE_MOBILE_NO=mobile_no,
                    EMPLOYEE_ADDRESS=address,
                    EMPLOYEE_IP=ip_address,
                    EMPLOYEE_ROLE=role,
                    EMPLOYEE_PASSWORD=password,
                    EMPLOYEE_CREATED_BY=request.session.get('employee_name', 'Admin')
                )
                
                return JsonResponse({
                    'status': 'success',
                    'message': 'Employee added successfully',
                    'employee': {
                        'id': employee.id,
                        'full_name': employee.EMPLOYEE_FULL_NAME,
                        'email': employee.EMPLOYEE_EMAIL,
                        'mobile_no': employee.EMPLOYEE_MOBILE_NO,
                        'address': employee.EMPLOYEE_ADDRESS,
                        'role': employee.EMPLOYEE_ROLE,
                        'created_at': employee.EMPLOYEE_CREATED_AT.strftime('%Y-%m-%d %H:%M')
                    }
                })
        
        return JsonResponse({'status': 'error', 'message': 'Invalid request'})


#!- UNIT SETUP VIEW PROTECTED WITH ADVANCE SECURITY WRAPPER
@method_decorator(advance_security_wrapper(allowed_roles=['ADMIN', 'MANAGER']), name='dispatch')
class UnitSetupView(View):

    def get(self, request):
        page = request.GET.get('page', 1)
        units = UnitSetup.objects.all().order_by('-UNIT_CREATED_AT')
        paginator = Paginator(units, 50)
        units_page = paginator.get_page(page)
        
        context = {
            'units': units_page,
            'total_units': units.count(),
            'page_range': paginator.get_elided_page_range(page, on_each_side=2, on_ends=1)
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
            
            unit_id = request.POST.get('unit_id', '').strip()
            unit_name = request.POST.get('unit_name', '').strip()
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
            
            try:
                created_by = EmployeeSetup.objects.get(id=request.session.get('employee_id')) if request.session.get('employee_id') else None
            except:
                created_by = None
            
            if unit_id:
                try:
                    unit = UnitSetup.objects.get(id=unit_id)
                    unit.UNIT_NAME = unit_name
                    unit.UNIT_SYMBOL = unit_symbol
                    unit.UNIT_MODIFIED_BY = created_by
                    unit.save()
                    return JsonResponse({'status': 'success', 'message': 'Unit updated successfully'})
                except UnitSetup.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'Unit not found'})
            else:
                unit = UnitSetup.objects.create(
                    UNIT_NAME=unit_name,
                    UNIT_SYMBOL=unit_symbol,
                    UNIT_CREATED_BY=created_by
                )
                return JsonResponse({'status': 'success', 'message': 'Unit added successfully'})
        
        return JsonResponse({'status': 'error', 'message': 'Invalid request'})


#!- PRODUCT CATEGORY VIEW PROTECTED WITH ADVANCE SECURITY WRAPPER
@method_decorator(advance_security_wrapper(allowed_roles=['ADMIN', 'MANAGER']), name='dispatch')
class ProductCategoryView(View):

    def get(self, request):
        page = request.GET.get('page', 1)
        categories = ProductCategory.objects.all().order_by('-CATEGORY_CREATED_AT')
        paginator = Paginator(categories, 50)
        categories_page = paginator.get_page(page)
        
        context = {
            'categories': categories_page,
            'total_categories': categories.count(),
            'page_range': paginator.get_elided_page_range(page, on_each_side=2, on_ends=1)
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
                    return JsonResponse({'status': 'success', 'message': 'Category deleted successfully'})
                except ProductCategory.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'Category not found'})
            
            category_id = request.POST.get('category_id', '').strip()
            category_name = request.POST.get('category_name', '').strip()
            
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
            
            try:
                created_by = EmployeeSetup.objects.get(id=request.session.get('employee_id')) if request.session.get('employee_id') else None
            except:
                created_by = None
            
            if category_id:
                try:
                    category = ProductCategory.objects.get(id=category_id)
                    category.CATEGORY_NAME = category_name
                    category.CATEGORY_MODIFIED_BY = created_by
                    category.save()
                    return JsonResponse({'status': 'success', 'message': 'Category updated successfully'})
                except ProductCategory.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'Category not found'})
            else:
                category = ProductCategory.objects.create(
                    CATEGORY_NAME=category_name,
                    CATEGORY_CREATED_BY=created_by
                )
                return JsonResponse({'status': 'success', 'message': 'Category added successfully'})
        
        return JsonResponse({'status': 'error', 'message': 'Invalid request'})


#!- PRODUCT SETUP VIEW PROTECTED WITH ADVANCE SECURITY WRAPPER
@method_decorator(advance_security_wrapper(allowed_roles=['ADMIN', 'MANAGER']), name='dispatch')
class ProductSetupView(View):

    def get(self, request):
        page = request.GET.get('page', 1)
        products = ProductSetup.objects.all().order_by('-PRODUCT_CREATED_AT')
        paginator = Paginator(products, 50)
        products_page = paginator.get_page(page)
        
        context = {
            'products': products_page,
            'total_products': products.count(),
            'units': UnitSetup.objects.all(),
            'categories': ProductCategory.objects.all(),
            'page_range': paginator.get_elided_page_range(page, on_each_side=2, on_ends=1)
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
                    return JsonResponse({'status': 'success', 'message': 'Product deleted successfully'})
                except ProductSetup.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'Product not found'})
            
            product_id = request.POST.get('product_id', '').strip()
            product_name = request.POST.get('product_name', '').strip()
            product_unit = request.POST.get('product_unit', '').strip()
            product_category = request.POST.get('product_category', '').strip()
            product_price = request.POST.get('product_price', '').strip()
            product_description = request.POST.get('product_description', '').strip()
            product_image = request.FILES.get('product_image')
            
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
                    float(product_price)
                    if float(product_price) <= 0:
                        errors['product_price'] = 'Price must be greater than 0'
                except ValueError:
                    errors['product_price'] = 'Price must be a valid number'
            
            if not product_description:
                errors['product_description'] = 'Description is required'
            
            if errors:
                return JsonResponse({'status': 'error', 'message': 'Please fix the highlighted fields', 'errors': errors})
            
            try:
                created_by = EmployeeSetup.objects.get(id=request.session.get('employee_id')) if request.session.get('employee_id') else None
                unit = UnitSetup.objects.get(id=product_unit)
                category = ProductCategory.objects.get(id=product_category)
            except UnitSetup.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Invalid unit selected'})
            except ProductCategory.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Invalid category selected'})
            except:
                created_by = None
            
            if product_id:
                try:
                    product = ProductSetup.objects.get(id=product_id)
                    product.PRODUCT_NAME = product_name
                    product.PRODUCT_UNIT = unit
                    product.PRODUCT_CATEGORY = category
                    product.PRODUCT_PRICE = product_price
                    product.PRODUCT_DESCRIPTION = product_description
                    if product_image:
                        product.PRODUCT_IMAGE = product_image
                    product.PRODUCT_MODIFIED_BY = created_by
                    product.save()
                    return JsonResponse({'status': 'success', 'message': 'Product updated successfully'})
                except ProductSetup.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'Product not found'})
            else:
                product = ProductSetup.objects.create(
                    PRODUCT_NAME=product_name,
                    PRODUCT_UNIT=unit,
                    PRODUCT_CATEGORY=category,
                    PRODUCT_PRICE=product_price,
                    PRODUCT_DESCRIPTION=product_description,
                    PRODUCT_IMAGE=product_image,
                    PRODUCT_CREATED_BY=created_by
                )
                return JsonResponse({'status': 'success', 'message': 'Product added successfully'})
        
        return JsonResponse({'status': 'error', 'message': 'Invalid request'})



