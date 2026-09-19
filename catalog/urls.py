from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('white-friday/', views.white_friday, name='white_friday'),
    path('<slug:slug>/', views.product_detail, name='product_detail'),
]
