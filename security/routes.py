from django.urls import path
from . import views

#!- SECURITY AND AUTHENTICATION ROUTE PATTERNS
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.PublicRegisterView.as_view(), name='register'),

    #-- CUSTOMER PASSWORD RESET FLOW ---
    path('password-reset/', views.PasswordResetRequestView.as_view(), name='password_reset'),
    path('password-reset/done/', views.PasswordResetSentView.as_view(), name='password_reset_done'),
    path('password-reset/confirm/<str:uidb64>/<str:token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

