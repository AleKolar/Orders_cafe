# mycafe/urls.py
from django.contrib import admin
from django.urls import path, include

from orders.views import ApiRoot, OrderViewSet, ItemViewSet, OrderUpdateStatusView, OrderListView, \
    search_orders_by_tables, menu

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ApiRoot.as_view(), name='api-root'),  # Корневой маршрут API
    path('api/', include('orders.urls')),  # Включаем маршруты из orders.urls


    path('orders/search/', OrderListView.as_view(), name='search'),

    path('search_orders_by_tables/', search_orders_by_tables, name='search_orders'),
    path('orders_by_tables/', OrderListView.as_view(), name='table_order_list'),

    path('menu/', menu, name='menu'), # Пользовательский интерфейс

    #path('orders/', OrderViewSet.as_view({'post': 'create'}), name='create_order'), #


]






