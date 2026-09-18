from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('confirmation/<int:order_id>/', views.confirmation, name='confirmation'),
    path('history/', views.history, name='history'),
    path('<int:order_id>/', views.detail, name='detail'),
]
