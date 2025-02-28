# mycafe/urls.py
from django.contrib import admin
from django.urls import path, include

from orders.views import ApiRoot, OrderViewSet, ItemViewSet, OrderUpdateStatusView, OrderListView, \
    search_orders_by_tables

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ApiRoot.as_view(), name='api-root'),  # Корневой маршрут API
    path('api/', include('orders.urls')),  # Включаем маршруты из orders.urls


    # path('menu/create/', OrderViewSet.as_view({'post': 'create'}), name='create_order'),
    #
    # path('api/products/', ItemViewSet.as_view({'post': 'create'}), name='api_products_create'),
    #
    # path('api/orders/<int:id>', OrderViewSet.as_view({'delete': 'destroy'}), name='api_orders_delete'),
    #
    # path('api/orders/update_status/<int:id>/', OrderUpdateStatusView.as_view({'patch': 'update_status'}), name='api_orders_update_status'),

    path('search_orders_by_tables/', search_orders_by_tables, name='search_orders'),
    path('orders_by_tables/', OrderListView.as_view(), name='table_order_list'),

    path('menu/', OrderUpdateStatusView.as_view({'get': 'menu'}), name='menu'),
    path('orders/', OrderViewSet.as_view({'post': 'create'}), name='create_order'),


]






