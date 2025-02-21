# orders/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Order
from .forms import OrderForm
from django.http import HttpResponse


def order_list(request):
    """
    Отображает список всех заказов с возможностью фильтрации по статусу.

    Args:
        request: HTTP запрос от клиента.

    Returns:
        HttpResponse: Ответ с отображением списка заказов.
    """
    status_filter = request.GET.get('status')  # Получаем статус из GET-запроса
    orders = Order.objects.all()

    if status_filter:
        orders = orders.filter(status=status_filter)  # Фильтруем заказы по статусу

    return render(request, 'orders/order_list.html', {'orders': orders})

def order_create(request):
    """
    Создает новый заказ.

    Этот представление обрабатывает создание нового заказа путем приема
    POST-запроса с данными формы. Если данные формы валидны, заказ
    сохраняется в базе данных и происходит перенаправление на страницу
    со списком заказов.

    Args:
        request: HTTP запрос от клиента.

    Returns:
        HttpResponse: Ответ с формой для создания нового заказа или перенаправление на
        страницу со списком заказов после успешного сохранения.
    """
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderForm()
    return render(request, 'orders/order_form.html', {'form': form})

def order_delete(request, pk):
    """
    Удаляет существующий заказ.

    Этот представление удаляет заказ с заданным первичным ключом (pk) из
    базы данных. Если заказ не найден, возвращает 404 ошибку.
    После удаления происходит перенаправление на страницу со списком заказов.

    Args:
        request: HTTP запрос от клиента.
        pk (int): Первичный ключ заказа, который необходимо удалить.

    Returns:
        HttpResponse: Перенаправление на страницу со списком заказов после успешного удаления.
    """
    order = get_object_or_404(Order, pk=pk)
    order.delete()
    return redirect('order_list')

def order_update(request, pk):
    """
    Обновляет существующий заказ.

    Этот представление обрабатывает обновление заказа с заданным первичным
    ключом (pk). Если запрос POST, проверяет данные формы и сохраняет измененный
    заказ. В противном случае отрисовывает форму с текущими данными заказа.

    Args:
        request: HTTP запрос от клиента.
        pk (int): Первичный ключ заказа, который необходимо обновить.

    Returns:
        HttpResponse: Ответ с формой для обновления заказа или перенаправление
        на страницу со списком заказов после успешного обновления.
    """
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderForm(instance=order)
    return render(request, 'orders/order_form.html', {'form': form})