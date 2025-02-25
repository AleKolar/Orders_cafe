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
        fields = '__all__'