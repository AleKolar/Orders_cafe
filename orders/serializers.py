# serializers.py
from rest_framework import serializers
from .models import Order, Items


class OrderSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = Order  
        fields = ['table_number', 'items', 'total_price', 'status', 'created_at']

class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = '__all__'