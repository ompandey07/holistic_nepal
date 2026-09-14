from . import views
from django.urls import path



urlpatterns = [

    # -- ADMIN ROUTES ---


    # -- DASHBOARD PAGE ---
    path('dashboard/', views.AdminDashboardView.as_view(), name='admin_dashboard'),


    
]