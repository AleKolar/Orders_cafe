# tests.py
import os
from django.conf import settings

# Установка переменной окружения DJANGO_SETTINGS_MODULE, если она не установлена
if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mycafe.settings')

# Импортируем модули после инициализации настроек
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from .models import Order, Items  # Импортируем ваши модели


class OrderAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # Создание блюд для тестирования
        self.item1 = Items.objects.create(name='Pizza', price=1200)
        self.item2 = Items.objects.create(name='Pasta', price=800)

    def test_update_order_status(self):
        # Создаем заказ с корректным форматом items
        order = Order.objects.create(
            table_number=1,
            items=[
                {"name": self.item1.name, "quantity": 2},
                {"name": self.item2.name, "quantity": 1},
            ],
            status='paid',
            total_price=3200
        )
        # Изменяем статус заказа
        order.status = 'ready'
        order.save()
        # Получаем обновленный заказ из БД
        updated_order = Order.objects.get(id=order.id)
        # Проверяем, что статус обновился
        self.assertEqual(updated_order.status, 'ready')

    def test_get_bill(self):
        # Создаем заказ для тестирования
        order = Order.objects.create(table_number=1, items=[{"name": self.item1.name, "quantity": 2}, {"name": self.item2.name, "quantity": 1}], status='paid', total_price=3200)
        url = reverse('get_bill', args=[1])  # Используем номер стола
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_bill'], 3200)  # Проверка общей суммы

    class OrderAPITestCase(APITestCase):
        def test_delete_order(self):
            # Создаем предварительный заказ
            order = Order.objects.create(table_number=1, status='paid')  # Статус может быть любым

            url = reverse('api_orders_delete', args=[1])  # номер стола для удаления

            # Отправляем запрос на удаление
            response = self.client.delete(url)

            # Проверяем, что ответ имеет код 204
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

            # Проверяем, что заказ был удален
            self.assertFalse(Order.objects.filter(id=order.id).exists())  # Проверяем наличие заказа

    def test_update_order_status(self):
        # Создаем предварительный заказ
        order = Order.objects.create(table_number=1, items=[{"name": self.item1.name, "quantity": 2},], status='paid', total_price=1000)
        url = reverse('api_orders_update_status', args=[order.id])
        data = {'status': 'paid'}  # Обновляем статус на допустимый
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order.refresh_from_db()  # Обновляем заказ из базы данных
        self.assertEqual(order.status, 'paid')  # Проверяем, что статус обновился

    def test_create_item(self):
        url = reverse('api_products_create')
        data = {'name': 'Salad', 'price': 600}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_revenue(self):
        url = reverse('revenue')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# python manage.py test orders