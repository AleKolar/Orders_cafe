# admin.py
from django.contrib import admin
from .models import Order

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'table_number', 'total_price', 'status', 'created_at')  # Поля интерфейса
    search_fields = ('table_number', 'status')  # Поиск по номеру стола и статусу
    list_filter = ('status',)  # Фильтры по статусу

admin.site.register(Order, OrderAdmin)
