
from django import forms
from django.forms import modelformset_factory
from .models import MenuItem, Order, OrderItem


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'price']


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['menu_item', 'quantity']


OrderItemFormSet = modelformset_factory(OrderItem, form=OrderItemForm, extra=1, can_delete=True)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = []  # Убираем поле table_number, чтобы не путать пользователей


class OrderAdminForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['table_number', 'status', 'items',
                  'total_price']  # Включаем поля для номера стола, статуса, блюд и итоговой стоимости.

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['items'].queryset = MenuItem.objects.all()  # Определяем доступные блюда
        # В случае, если экземпляр заказа уже существует, устанавливаем значение total_price
        if self.instance and self.instance.pk:
            self.fields['total_price'].initial = self.instance.total_price

    def save(self, commit=True):
        order = super().save(commit=False)
        # Предположим, что у вас есть связь many-to-many между Order и MenuItem
        total = sum(item.menu_item.price * item.quantity for item in
                    order.items.all())  # Здесь нужно написать метод для вычисления цены
        order.total_price = total  # Обновляем сумму заказа
        if commit:
            order.save()  # Сохраняем изменения
        return order