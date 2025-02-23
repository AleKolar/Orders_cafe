from django.db.models import Sum
from rest_framework import viewsets
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from .models import Order
from .serializers import OrderSerializer
from rest_framework.response import Response
from rest_framework import status

class OrderViewSet(viewsets.ModelViewSet):
    """
    Manage orders in the system.
    This endpoint allows you to create, retrieve, update, and delete orders.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def list(self, request):  # Получение списка всех заказов

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):  # Получение заказа по ID
        """
        Retrieve a list of all orders.
        """
        order = self.get_object()
        serializer = self.get_serializer(order)
        return Response(serializer.data)

    def create(self, request):  # Создание нового заказа
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):  # Обновление существующего заказа
        order = self.get_object()
        serializer = self.get_serializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):  # Удаление заказа
        order = self.get_object()
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class RevenueView(APIView):  # Расчет выручки за смену
    def get(self, request):
        total_revenue = Order.objects.filter(status='paid').aggregate(Sum('total_price'))['total_price'] or 0
        return Response({'total_revenue': total_revenue})

class ApiRoot(APIView):
    """
    API root view.
    Returns links to the available API endpoints, including the list of orders and Swagger documentation.
    """
    def get(self, request, format=None):
        return Response({
            'orders': reverse('order-list', request=request, format=format),
            'swagger': reverse('schema-swagger-ui', request=request, format=format),
        })