# orders/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum
from django.urls import reverse
from .models import Order, Items, OrderItems  # Убедитесь, что названия совпадают
from .serializers import OrderSerializer, ItemsSerializer

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum
from django.urls import reverse
from .models import Order, Items
from .serializers import OrderSerializer, ItemsSerializer

class OrderViewSet(viewsets.ModelViewSet):
    """ Управление заказами в системе """
    queryset = Order.objects.all()  # Получаем все заказы
    serializer_class = OrderSerializer  # Указываем сериализатор

    # Получение списка заказов
    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # Получение конкретного заказа по его ID
    def retrieve(self, request, pk=None):
        order = self.get_object()
        serializer = self.get_serializer(order)
        return Response(serializer.data)

    # Создание нового заказа
    def create(self, request):
        # Извлекаем данные из запроса
        table_number = request.data.get('table_number')
        items_data = request.data.get('items')  # Ожидаем список блюд с количеством

        # Проверяем валидность table_number
        if not isinstance(table_number, int):
            return Response({"error": "Номер стола должен быть целым числом."}, status=status.HTTP_400_BAD_REQUEST)

        # Проверяем, что items_data не пустой
        if not items_data or not isinstance(items_data, list):
            return Response({"error": "Список блюд не может быть пустым и должен быть списком."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Создаем новый заказ
        order = Order(table_number=table_number, status="в ожидании")
        order.save()  # Сохраняем заказ, чтобы получить его ID

        total_price = 0  # Инициализируем общую стоимость
        items_list = []  # Список для хранения блюд и количеств

        # Обрабатываем каждое блюдо
        for data in items_data:
            item_id = data.get('id')  # ID блюда
            quantity = data.get('quantity', 1)  # Количество, по умолчанию 1

            # Получаем блюдо из базы данных
            try:
                item = Items.objects.get(id=item_id)
            except Items.DoesNotExist:
                return Response({"error": f"Блюдо с ID {item_id} не найдено."}, status=status.HTTP_404_NOT_FOUND)

            # Увеличиваем общую стоимость
            total_price += item.price * quantity
            items_list.append({'id': item_id, 'quantity': quantity})  # Добавляем информацию о блюде в список

        # Сохраняем данные о блюдах в JSONField
        order.items = items_list
        order.total_price = total_price
        order.save()  # Сохраняем заказ с обновленной стоимостью и данными о блюдах

        # Сериализуем и возвращаем данные нового заказа
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, table_number=None):
        try:
            order = self.get_object(table_number)  # Получаем объект заказа по номеру стола
        except Order.DoesNotExist:
            return Response({"error": "Заказ не найден."}, status=status.HTTP_404_NOT_FOUND)

        table_number = request.data.get('table_number',
                                        order.table_number)  # Сохраняем старое значение, если новое не передано
        items_data = request.data.get('items')  # Ожидаем список блюд с количеством

        # Удаляем старые записи, если передан новый список блюд
        if items_data is not None:
            order.orderitems_set.all().delete()  # Удаляем старые позиции заказа

            total_price = 0  # Инициализируем общую стоимость

            # Пройдёмся по каждому блюду в новом списке
            for data in items_data:
                item_id = data.get('id')  # ID блюда
                quantity = data.get('quantity', 1)  # Количество, по умолчанию 1

                # Получаем блюдо из базы данных
                try:
                    item = Items.objects.get(id=item_id)
                except Items.DoesNotExist:
                    return Response({"error": f"Блюдо с ID {item_id} не найдено."}, status=status.HTTP_404_NOT_FOUND)

                # Создаем запись в промежуточной модели OrderItems
                order_item = OrderItems(order=order, items=item, quantity=quantity)
                order_item.save()

                # Увеличиваем общую стоимость
                total_price += item.price * quantity

            # Устанавливаем общую стоимость заказа
            order.total_price = total_price

        # Обновляем номер стола, если он передан
        if table_number is not None:
            order.table_number = table_number

        order.save()  # Сохраняем обновленный заказ

        # Сериализуем и возвращаем данные обновленного заказа
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    # Удаление заказа по номеру стола
    def destroy(self, request, table_number=None):
        # Ищем заказ по номеру стола
        try:
            order = Order.objects.get(table_number=table_number)
            order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Order.DoesNotExist:
            return Response({"error": "Заказ с данным номером стола не найден."}, status=status.HTTP_404_NOT_FOUND)


class ItemsViewSet(viewsets.ModelViewSet):
    """ Блюда: добавление блюд и цен на них """
    queryset = Items.objects.all()  # Правильный класс
    serializer_class = ItemsSerializer  # Правильный сериализатор

    # Создание/Добавление нового блюда и цены на него
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RevenueView(APIView):
    """ Вычисление выручки от оплаченных заказов """
    def get(self, request):
        total_revenue = Order.objects.filter(status='paid').aggregate(Sum('total_price'))['total_price'] or 0  # Считаем общую выручку
        return Response({'total_revenue': total_revenue})


class ApiRoot(APIView):
    """ Корневая точка API.
    Возвращает ссылки на доступные конечные точки API, включая списки заказов, продуктов, выручки и документацию Swagger.
    """
    def get(self, request, format=None):
        return Response({
            'orders': reverse('order-list'),  # Ссылка на список заказов
            'items': reverse('product-list'),  # Ссылка на список блюд
            'revenue': reverse('revenue'),  # Ссылка на выручку
            'swagger': reverse('schema-swagger-ui'),  # Ссылка на Swagger документацию
        })