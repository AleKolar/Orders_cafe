from django.contrib import admin

from .forms import OrderAdminForm
from .models import MenuItem, Order, OrderItem

class OrderAdmin(admin.ModelAdmin):
    form = OrderAdminForm  # Используем нашу пользовательскую форму

    list_display = ('id', 'table_number', 'status', 'created_at')  # Настройка отображаемых полей
    list_filter = ('status',)  # Фильтрация по статусу
    search_fields = ('table_number',)  # Поиск по номеру стола

# Регистрация моделей
admin.site.register(MenuItem)  # Регистрируем MenuItem
admin.site.register(OrderItem)  # Регистрируем OrderItem
admin.site.register(Order, OrderAdmin)  # Регистрируем Order с админским интерфейсом
