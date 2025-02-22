from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, MenuItem, OrderItem
from .forms import MenuItemForm, OrderForm, OrderItemForm, OrderItemFormSet
from django.contrib.auth.decorators import login_required, user_passes_test


def home(request):
    return render(request, 'home.html')

# Декоратор для проверки администратора
def admin_required(view_func):
    return user_passes_test(lambda u: u.is_superuser)(view_func)

# 1. Список блюд
def menu_item_list(request):
    items = MenuItem.objects.all()
    return render(request, 'menu_item_list.html', {'items': items})

# 2. Создание нового блюда (администратор)
@admin_required
def create_menu_item(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu_item_list')
    else:
        form = MenuItemForm()
    return render(request, 'create_menu_item.html', {'form': form})

# 3. Список всех заказов
@admin_required
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'order_list.html', {'orders': orders})


def create_order(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        order_item_formset = OrderItemFormSet(request.POST)

        if order_form.is_valid() and order_item_formset.is_valid():
            order = order_form.save()
            order_items = order_item_formset.save(commit=False)
            for item in order_items:
                item.order = order  # Связываем с заказом
                item.save()
    # Редирект на страницу после успешного создания заказа
    else:
        order_form = OrderForm()
        order_item_formset = OrderItemFormSet(queryset=OrderItem.objects.none())

    context = {
        'order_form': order_form,
        'order_item_formset': order_item_formset,
    }
    return render(request, 'create_order.html', context)


# 5. Изменение статуса заказа
@admin_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order.status = request.POST.get('status')
        order.save()
        return redirect('order_list')

    return render(request, 'update_order_status.html', {'order': order})

# 6. Удаление заказа
@admin_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    return redirect('order_list')

# 7. Расчет выручки
@admin_required
def revenue(request):
    total_revenue = sum(order.total_price for order in Order.objects.filter(status='paid'))
    return render(request, 'revenue.html', {'total_revenue': total_revenue})