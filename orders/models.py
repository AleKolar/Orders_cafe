from django.db import models

class MenuItem(models.Model):
    name = models.CharField(max_length=100)  # Название блюда
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена

    def __str__(self):
        return f"{self.name} - {self.price} ₽"

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('ready', 'Готово'),
        ('paid', 'Оплачено'),
    ]

    table_number = models.IntegerField()
    items = models.ManyToManyField(MenuItem, through='OrderItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - Table {self.table_number}"

    def calculate_total_price(self):
        self.total_price = sum(item.get_total_price() for item in self.orderitem_set.all())
        self.save()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.menu_item.price * self.quantity

    def __str__(self):
        return f"{self.menu_item.name} (x{self.quantity})"
