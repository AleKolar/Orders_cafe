# orders/views.py
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum, Q
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend

from .filters import OrderFilter
from .forms import TableSearchForm
from .models import Order, Items
from .serializers import OrderSerializer, OrderCreateSerializer, ItemsSerializerProducts, \
    OrderStatusUpdateSerializer



class OrderViewSet(viewsets.ModelViewSet):
    """ Управление заказами в системе """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    # Получение списка заказов
    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # Получение конкретного заказа по его ID
    def retrieve(self, request, pk=id):
        order = self.get_object()
        serializer = self.get_serializer(order)
        return Response(serializer.data)

    # Создание нового заказа
    def create(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):  # Валидация и выброс исключения
            table_number = serializer.validated_data['table_number']
            items_data = serializer.validated_data['items']  # Получаем уже валидированные данные

            total_price = 0
            items_list = []

            for data in items_data:
                item_id = data.get('id')
                quantity = data.get('quantity', 1)

                try:
                    item = Items.objects.get(id=item_id)
                except Items.DoesNotExist:
                    return Response({"error": f"Блюдо с ID {item_id} не найдено."}, status=status.HTTP_404_NOT_FOUND)

                total_price += item.price * quantity
                items_list.append({'id': item.id, 'name': item.name, 'price': item.price, 'quantity': quantity})  # Сохраняем данные, как они есть в Item

            order = Order.objects.create(
                table_number=table_number,
                status="в ожидании", # Или другое значение по умолчанию
                items=items_list,
                total_price=total_price
            )

            serializer = OrderCreateSerializer(order) # OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # Возвращаем ошибки сериализатора

    def update(self, request, pk=id, partial=True):
        try:
            order = self.get_object()  # Получаем объект заказа
        except Order.DoesNotExist:
            return Response({"error": "Заказ не найден."}, status=status.HTTP_404_NOT_FOUND)

        # Обновляем номер стола, если он передан
        table_number = request.data.get('table_number')
        if table_number is not None:
            order.table_number = table_number

            # Обновляем статус заказа, если он передан
        status_value = request.data.get('status')
        if status_value is not None:
            order.status = status_value  # Обновляем статус заказа

        # Обновляем блюда заказа, если они переданы
        items_data = request.data.get('items')
        if items_data is not None:
            total_price = 0
            items_list = []

            for item_data in items_data:
                item_id = item_data.get('id')
                quantity = item_data.get('quantity', 1)
                try:
                    item = Items.objects.get(id=item_id)
                except Items.DoesNotExist:
                    return Response({"error": f"Блюдо с ID {item_id} не найдено."}, status=status.HTTP_404_NOT_FOUND)

                    # Добавляем блюда в список и считаем общую стоимость
                items_list.append({"id": item.id, "name": item.name, "price": item.price, "quantity": quantity})
                total_price += item.price * quantity

                # Обновляем список предметов и общую стоимость заказа
            order.items = items_list
            order.total_price = total_price

        order.save()  # Сохраняем изменения

        # Сериализуем и возвращаем обновленный заказ
        serializer = self.get_serializer(order)
        return Response(serializer.data)

    # total_price заказа со стола (по номеру стола)
    def get_bill(self, request, table_number=None):
        if table_number is None:
            return Response({"error": "Необходимо указать номер стола."}, status=status.HTTP_400_BAD_REQUEST)
            # Получаем заказы по номеру стола с помощью filter и Q для фильтрации по нескольким статусам
        orders = Order.objects.filter(
            Q(table_number=table_number) & (Q(status='в ожидании') | Q(status='paid') | Q(status='ready'))
        )
        # Проверяем, есть ли заказы
        if not orders.exists():
            return Response({"error": "Заказов для этого номера стола не найдено."}, status=status.HTTP_404_NOT_FOUND)
            # Считаем общую сумму
        total_bill = sum(order.total_price for order in orders)
        # Возвращаем результат
        return Response({"table_number": table_number, "total_bill": total_bill})

        # Удаление заказа по номеру стола
    def destroy(self, request, pk=id):
        # Ищем заказ по номеру стола
        try:
            order = Order.objects.get(id=pk)
            order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Order.DoesNotExist:
            return Response({"error": "Заказ с данным номером стола не найден."}, status=status.HTTP_404_NOT_FOUND)


class OrderUpdateStatusView(viewsets.ModelViewSet):
    """Изменение статуса заказа"""
    serializer_class = OrderStatusUpdateSerializer  # serializer_class
    queryset = Order.objects.all()  # !!! Обязательно для ModelViewSet !!!
    def update_status(self, request, id):
        try:
            order = Order.objects.get(pk=id)
        except Order.DoesNotExist:
            return Response({'error': 'Заказ не найден'}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderStatusUpdateSerializer(order, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()  # Сохраняем обновленный статус
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class OrderUpdateStatusAPIView(APIView):
    """Изменение статуса заказа"""
    serializer_class = OrderStatusUpdateSerializer  # serializer_class
    queryset = Order.objects.all()  # !!! Обязательно для ModelViewSet !!!
    def update_status(self, request, id):
        try:
            order = Order.objects.get(pk=id)
        except Order.DoesNotExist:
            return Response({'error': 'Заказ не найден'}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderStatusUpdateSerializer(order, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()  # Сохраняем обновленный статус
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemViewSet(viewsets.ModelViewSet):
    """ Блюда: добавление блюд и цен на них """
    queryset = Items.objects.all()  # Правильный класс
    serializer_class = ItemsSerializerProducts  # Правильный сериализатор

    # Создание/Добавление нового блюда и цены на него
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class RevenueView(APIView):
    """ Вычисление выручки от оплаченных заказов """
    def get(self, request):
        # Вычисляем общую выручку от оплаченных заказов
        total_revenue_result = Order.objects.filter(status='paid').aggregate(total_revenue=Sum('total_price'))

        # Получаем значение выручки, если оно существует, иначе используем 0
        total_revenue = total_revenue_result.get('total_revenue', 0) or 0

        return Response({'total_revenue': total_revenue})

# class ApiRoot(APIView):
#     """ Корневая точка API.
#     Возвращает ссылки на доступные конечные точки API, включая списки заказов, продуктов, выручки и документацию Swagger.
#     """
#     def get(self, request, format=None):
#         return Response({
#             'orders': reverse('order-list'),  # Ссылка на список заказов
#             'items': reverse('product-list'),  # Ссылка на список блюд
#             'revenue': reverse('revenue'),  # Ссылка на выручку
#             'swagger': reverse('schema-swagger-ui'),  # Ссылка на Swagger документацию
#         })

class OrderListView(generics.ListAPIView):
    """ Поиск по заданным параметрам """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend] # DjangoRestFramework предоставляет DjangoFilterBackend для фильтрации
    filterset_class = OrderFilter


def search_orders_by_tables(request):
    if request.method == 'POST':
        form = TableSearchForm(request.POST)
        if form.is_valid():
            table_number = form.cleaned_data['table_number']
            orders = Order.objects.filter(table_number=table_number, status__in=['В ожидании', 'pending', 'Оплачено', 'paid', 'Готово', 'ready'])
            total_bill = sum(order.total_price for order in orders)

            return render(request, 'table_order_list.html',
                          {'orders': orders, 'total_bill': total_bill, 'table_number': table_number})
    else:
        form = TableSearchForm()

    return render(request, 'search_orders.html', {'form': form})


class ApiRoot(APIView):
    """ Пользовательский интерфейс """
    def get(self, request, *args, **kwargs):
        return render(request, 'api_root.html')