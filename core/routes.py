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

    # -- NEWS ROUTES ---
    path('news/', views.NewsListPageView(), name='news_list'),
    path('news/<slug:slug>/', views.NewsDetailPageView(), name='news_detail'),

    # -- HOLISTIC HOSPITAL ROUTE ---
    path('hospital/', views.HospitalPageView(), name='hospital'),

    # -- DEDICATED CLINICAL SERVICE DETAIL ROUTE ---
    path('services/<slug:slug>/', views.HospitalServiceDetailView.as_view(), name='service_detail'),

    # -- BOTANICAL GALLERY SHOWCASE ROUTE ---
    path('gallery/', views.GalleryPageView.as_view(), name='gallery'),

    # -- SHOPPING BASKET / CART ROUTES ---
    path('cart/', views.CartPageView(), name='cart'),
    path('cart/add/', views.AddToCartAPIView(), name='cart_add'),
    path('cart/update/', views.UpdateCartAPIView(), name='cart_update'),
    path('cart/remove/', views.RemoveFromCartAPIView(), name='cart_remove'),
    path('cart/count/', views.CartCountAPIView(), name='cart_count'),

    # -- CHECKOUT ROUTE (LOGIN PROTECTED) ---
    path('checkout/', views.CheckoutPageView(), name='checkout'),

    # -- DEDICATED PUBLIC ORDER TRACKING ROUTE ---
    path('track-order/', views.TrackOrderPageView.as_view(), name='track_order'),
]