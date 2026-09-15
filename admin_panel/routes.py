from . import views
from django.urls import path



urlpatterns = [

    # -- ADMIN ROUTES ---


    # -- DASHBOARD PAGE ---
    path('dashboard/', views.AdminDashboardView.as_view(), name='admin_dashboard'),

    # -- EMPLOYEE SETUP PAGE ---
    path('employee-setup/', views.EmployeeSetupView.as_view(), name='employee_setup'),

    # -- INVENTORY PAGES ---
    path('unit-setup/', views.UnitSetupView.as_view(), name='unit_setup'),
    path('product-category/', views.ProductCategoryView.as_view(), name='product_category'),
    path('product-setup/', views.ProductSetupView.as_view(), name='product_setup'),


    
]