from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', views.index, name='index'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token_refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('post/',views.create_post,name = 'post'),
    path('register/',views.register,name = 'register'),
    path('api/register/',views.registeruser,name = 'register_user'),
    path('login/',views.login,name='login'),
    path('reset/',views.reset,name='reset'),
    path('cart/', views.cart, name='cart'),
    path('place-order/', views.place_order, name='place_order'),
    path('order/', views.order, name='order'),
    path('order-success/', views.order_success, name='order_success'),
    path('<slug:slug>/', views.details, name='details'), 
    path('contact', views.contact, name='contact'),
    path('about', views.about, name='about'), 
    
    
]
