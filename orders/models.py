from django.db import models  

class Order(models.Model):  
    STATUS_CHOICES = [  
        ('pending', 'В ожидании'),  
        ('ready', 'Готово'),  
        ('paid', 'Оплачено'),  
    ]  

    table_number = models.IntegerField()  
    items = models.JSONField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):  
        # Автоматический расчет общей стоимости  
        self.total_price = sum(item['price'] for item in self.items)  
        super().save(*args, **kwargs)  

    def __str__(self):  
        return f'Order {self.id} at Table {self.table_number}'  