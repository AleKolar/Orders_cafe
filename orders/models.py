# models.py
from django.db import models

''' Определяем модели и их поля, что будем использовать при обработке заказов '''

class Items(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('ready', 'Готово'),
        ('paid', 'Оплачено'),
    ]

    table_number = models.IntegerField()
    items = models.JSONField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Добавляем поле для цены


    def save(self, *args, **kwargs):
        total_price = sum(order_product.product.price * order_product.quantity for order_product in self.orderproduct_set.all())
        self.total_price = total_price
        super().save(*args, **kwargs)


