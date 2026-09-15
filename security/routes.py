from django.urls import path
from . import views

#!- SECURITY AND AUTHENTICATION ROUTE PATTERNS
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.PublicRegisterView.as_view(), name='register'),
]
