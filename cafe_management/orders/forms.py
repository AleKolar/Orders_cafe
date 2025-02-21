# orders/forms.py
from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    """
    Форма для управления заказами.

    Эта форма предоставляет интерфейс для создания и обновления объектов
    модели Order. Она включает валидацию для полей формы.

    Attributes:
        Meta: Внутренний класс, который определяет модель и поля,
              используемые в форме.
    """

    class Meta:
        model = Order
        fields = ['table_number', 'items', 'status']  # Поля, которые будут отображаться в форме

    def clean_items(self):
        """
        Валидация поля 'items'.

        Проверяет, что поле 'items' является списком. Если нет,
        выдает ошибку валидации.

        Returns:
            list: Чистые данные для поля 'items'.

        Raises:
            ValidationError: Если 'items' не является списком.
        """
        items = self.cleaned_data.get('items')
        if not isinstance(items, list):
            raise forms.ValidationError("Items must be a list of dictionaries with 'name' and 'price'.")
        return items
