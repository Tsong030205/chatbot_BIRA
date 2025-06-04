from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('custom/', views.custom, name='custom'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('shop/', views.shop, name='shop'),
    path('services/', views.services, name='services'),
    path('careers/', views.placeholder, name='careers'),
    path('faq/', views.placeholder, name='faq'),
    path('privacy/', views.placeholder, name='privacy'),
    path('terms/', views.placeholder, name='terms'),
    path('cookies/', views.placeholder, name='cookies'),
    path('chatbot/', views.chatbot, name='chatbot'),
]