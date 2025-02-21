# orders/models.py
from django.db import models

class Order(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'В ожидании'),
        ('ready', 'Готово'),
        ('paid', 'Оплачено'),
    ]

    table_number = models.IntegerField()
    items = models.JSONField()  # Список заказанных блюд в формате JSON
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='waiting')
    created_at = models.DateTimeField(auto_now_add=True)  # Для отслеживания времени создания заказа

    def save(self, *args, **kwargs):
        # Дополнительная логика для автоматического расчета общей стоимости перед сохранением
        self.total_price = sum(item['price'] for item in self.items)  # Предполагаем, что items - это список словарей с ключом 'price'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.id} - Table {self.table_number}"
