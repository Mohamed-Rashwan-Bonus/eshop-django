from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='detail'),
    path('add/<int:product_id>/', views.cart_add, name='add'),
    path('increase/<int:product_id>/', views.cart_increase, name='increase'),
    path('decrease/<int:product_id>/', views.cart_decrease, name='decrease'),
    path('remove/<int:product_id>/', views.cart_remove, name='remove'),
    path('clear/', views.cart_clear, name='clear'),
]
