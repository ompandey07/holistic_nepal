from . import views
from django.urls import path



urlpatterns = [

    # -- CORE ROUTES ---


    # -- HOME PAGE ---
    path('', views.HomePageView(), name='home'),

    # -- OUR PRODUCTS PAGE ---
    path('products/', views.OurProductsPageView(), name='our_products'),

    # -- PRODUCT DETAIL PAGE ---
    path('product/<slug:slug>/', views.ProductDetailPageView(), name='product_detail'),



]