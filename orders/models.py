from django.db import models  

# models.py
from django.db import models

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
    items = models.ManyToManyField(Items, through='OrderItems')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    # def save(self, *args, **kwargs):
    #     total_price = 0
    #     for order_items in self.orderproduct_set.all():
    #         total_price += order_items.product.price * order_items.quantity
    #     self.total_price = total_price
    #     super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        total_price = sum(order_product.product.price * order_product.quantity for order_product in self.orderproduct_set.all())
        self.total_price = total_price
        super().save(*args, **kwargs)

class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    items = models.ForeignKey(Items, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

