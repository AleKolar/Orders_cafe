# mycafe/urls.py
from django.contrib import admin
from django.urls import path, include

from orders.views import ApiRoot

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ApiRoot.as_view(), name='api-root'),  # Корневой маршрут API
    path('api/', include('orders.urls')),  # Включаем маршруты из orders.urls


]

