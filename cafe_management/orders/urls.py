# orders/urls.py
from django.urls import path
from .views import order_list, order_create, order_delete, order_update

urlpatterns = [
    path('', order_list, name='order_list'),
    path('create/', order_create, name='order_create'),
    path('delete/<int:pk>/', order_delete, name='order_delete'),
    path('update/<int:pk>/', order_update, name='order_update'),
]