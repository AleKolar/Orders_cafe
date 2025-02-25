# orders/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import OrderViewSet, ItemsViewSet, RevenueView

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')  # Помним про - Регистрация OrderViewSet
router.register(r'products', ItemsViewSet, basename='product')  # Помним про - Регистрация ProductViewSet

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
]