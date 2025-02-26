# serializers.py
import logging

from rest_framework import serializers
from .models import Order, Items

logger = logging.getLogger(__name__)

class OrderSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = Order  
        fields = ['table_number', 'items', 'status', 'total_price']
        read_only_fields = ['total_price']

class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['table_number', 'items']
        read_only_fields = ['status', 'total_price']

class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = ['name', 'price', 'quantity']

class ItemsSerializerProducts(serializers.ModelSerializer):
    price = serializers.DecimalField(
        max_digits=10, decimal_places=2, coerce_to_string=True
    )

    class Meta:
        model = Items
        fields = ['name', 'price']

class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status', 'table_number', 'id']

    def validate_status(sels, value):
        logger.info(f"Проверка статуса: {value}")
        if value not in dict(Order.STATUS_CHOICES).keys():
            raise serializers.ValidationError("Неверный статус заказа.")
        return value

