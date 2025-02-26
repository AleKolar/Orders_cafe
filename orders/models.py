# models.py
from django.db import models

''' Определяем модели и их поля, что будем использовать при обработке заказов '''

class Items(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0.0)
    quantity = models.IntegerField(default=0)

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
    total_price = models.FloatField(default=0.0)


    def save(self, *args, **kwargs):
        total_price = 0.0
        for item in self.items:
            # Получаем цену блюда по имени
            try:
                item_instance = Items.objects.get(name=item['name'])
                total_price += item_instance.price * item['quantity']
            except Items.DoesNotExist:
                # Обработка случая, когда блюдо не найдено
                continue
        self.total_price = total_price
        super().save(*args, **kwargs)

    # def change_status(self, new_status):
    #     if new_status in dict(self.STATUS_CHOICES):
    #         self.status = new_status
    #         self.save()
    #         if new_status == 'paid':
    #             self.calculate_revenue()




