# mycafe/urls.py
from django.urls import path, include

from orders.views import ApiRoot

urlpatterns = [
    path('', ApiRoot.as_view(), name='api-root'),
    path('api/', include('orders.urls')),
]

