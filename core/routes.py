from . import views
from django.urls import path



urlpatterns = [

    # -- CORE ROUTES ---


    # -- HOME PAGE ---
    path('', views.HomePageView(), name='home'),


    
]