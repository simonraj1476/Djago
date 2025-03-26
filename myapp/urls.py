from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register_user/',views.registeruser,name = 'register_user'),
    path('register/',views.register,name = 'register'),
    path('login/',views.login,name='login'),
    path('reset/',views.reset,name='reset'),
    path('cart/', views.cart, name='cart'),
    path('order/', views.order, name='order'),
    path('<slug:slug>/', views.details, name='details'), 
    path('contact', views.contact, name='contact'),
    path('about', views.about, name='about'), 
    
    
]
