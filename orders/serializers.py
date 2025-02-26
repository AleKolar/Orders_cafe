# serializers.py
from rest_framework import serializers
from .models import Order, Items


class OrderSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = Order  
        fields = ['table_number', 'items', 'status', 'total_price']
        read_only_fields = ['total_price']

class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['table_number', 'items']

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