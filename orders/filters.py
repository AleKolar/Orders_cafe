# orders/filters.py
from django_filters import rest_framework as filters
from orders.models import Order

class OrderFilter(filters.FilterSet):
    table_number = filters.NumberFilter(field_name='table_number') # Фильтр по номеру стола
    status = filters.CharFilter(field_name='status') # Фильтр по статусу

    class Meta:
        model = Order
        fields = ['table_number', 'status']