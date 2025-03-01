# mycafe/urls.py
from django.contrib import admin
from django.urls import path, include

from orders.views import ApiRoot, OrderViewSet, ItemViewSet, OrderUpdateStatusView, OrderListView, \
    search_orders_by_tables, menu

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ApiRoot.as_view(), name='api-root'),  # Корневой маршрут API
    path('api/', include('orders.urls')),  # Включаем маршруты из orders.urls


    path('search_orders_by_tables/', search_orders_by_tables, name='search_orders'),
    path('orders_by_tables/', OrderListView.as_view(), name='table_order_list'),

    path('menu/', menu, name='menu'), # Пользовательский интерфейс

    path('menu/orders/', OrderViewSet.as_view({'post': 'create'}), name='create_order'), # Для работы пользовательского интерфейса
    path('menu/orders/<int:id>/update_status/', OrderUpdateStatusView.as_view({'patch': 'update_status'}), name='update_status'), # Для работы пользовательского интерфейса


    path('orders/create/', OrderViewSet.as_view({'post': 'create'}), name='create_order'),

    path('item/products/', ItemViewSet.as_view({'post': 'create'}), name='api_products_create'),

    path('orders/<int:pk>', OrderViewSet.as_view({'delete': 'destroy'}), name='api_orders_delete'),

    path('orders/update_status/<int:id>/', OrderUpdateStatusView.as_view({'patch': 'update_status'}), name='update_status'),

    path('orders/search/', OrderListView.as_view(), name='search'),
]







