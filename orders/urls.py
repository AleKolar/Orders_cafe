# orders/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import OrderViewSet, ItemViewSet, RevenueView, ApiRoot, OrderUpdateStatusView, OrderUpdateStatusAPIView, \
    OrderListView

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')  # Помним про - Регистрация OrderViewSet
router.register(r'products', ItemViewSet, basename='product')  # Помним про - Регистрация ProductViewSet

schema_view = get_schema_view(
   openapi.Info(
      title="Order API",
      default_version='v1',
      description="API для управления заказами",
   ),
   public=True,
)

urlpatterns = [
    path('', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('revenue/', RevenueView.as_view(), name='revenue'),  # Добавление маршрута для RevenueView ("Выручка")
    path('orders/bill/<int:table_number>/', OrderViewSet.as_view({'get': 'get_bill'}), name='get_bill'), # Добавление маршрута для "Счёт" со стола
    path('orders/update_status/<int:id>/', OrderUpdateStatusView.as_view({'patch': 'update_status'}), name='update_status'),# Обновление из Swagger
    path('', ApiRoot.as_view(), name='api-root'),

    path('orders/search', OrderListView.as_view(), name='search'),

    # URLS ДЛЯ ТЕСТОВ

    # path('orders/create/', OrderViewSet.as_view({'post': 'create'}), name='create_order'),
    #
    # path('products/', ItemViewSet.as_view({'post': 'create'}), name='api_products_create'),
    #
    # path('orders/<int:id>', OrderViewSet.as_view({'delete': 'destroy'}), name='api_orders_delete'),
    #
    # path('orders/update_status/<int:id>/', OrderUpdateStatusView.as_view({'patch': 'update_status'}), name='update_status'),



]