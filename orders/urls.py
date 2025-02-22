# orders/urls.py
from django.urls import path
from .views import (
    menu_item_list,
    create_menu_item,
    order_list,
    create_order,
    update_order_status,
    delete_order,
    revenue,
)

urlpatterns = [
    path('menu/', menu_item_list, name='menu_item_list'),
    path('menu/create/', create_menu_item, name='create_menu_item'),
    path('orders/', order_list, name='order_list'),
    path('orders/create/', create_order, name='create_order'),
    path('orders/update/<int:order_id>/', update_order_status, name='update_order_status'),
    path('orders/delete/<int:order_id>/', delete_order, name='delete_order'),
    path('orders/revenue/', revenue, name='revenue'),
]