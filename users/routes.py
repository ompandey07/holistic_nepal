from . import views
from django.urls import path


urlpatterns = [
    # -- USER DASHBOARD ROUTES --
    
    # -- USER DASHBOARD PAGE --
    path('dashboard/', views.UserDashboardView.as_view(), name='user_dashboard'),
    
    # -- USER ORDERS PAGE --
    path('orders/', views.UserOrdersView.as_view(), name='user_orders'),
    
    # -- USER SETTINGS PAGE --
    path('settings/', views.UserSettingsView.as_view(), name='user_settings'),
]