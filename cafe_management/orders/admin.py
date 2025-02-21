# orders/admin.py
from django.contrib import admin
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Административный интерфейс для управления заказами.
    Позволяет отображать, фильтровать, искать и управлять заказами , только, в административной панели.
    """

    list_display = ('id', 'table_number', 'total_price', 'status', 'created_at')
    search_fields = ('table_number', 'status')
    list_filter = ('status',)
    ordering = ('-id',)

    def get_total_revenue(self, request):
        """
        Вычисляет общий объем выручки за заказы со статусом 'оплачено'.

        Returns:
            Decimal: Общая сумма всех оплаченных заказов.
            Если оплаченных заказов нет, возвращает 0.
        """
        total_revenue = Order.objects.filter(status='paid').aggregate(Sum('total_price'))['total_price__sum']
        return total_revenue if total_revenue else 0

    def changelist_view(self, request, extra_context=None):
        """
        Переопределяет метод для отображения списка заказов.

        Добавляет общий объем выручки за смену в контекст для отображения на странице.

        Args:
            request: HTTP запрос.
            extra_context: Дополнительный контекст для передачи в шаблон.

        Returns:
            HttpResponse: Ответ с отображением списка заказов и выручки.
        """
        revenue = self.get_total_revenue(request)
        extra_context = extra_context or {}
        extra_context['total_revenue'] = revenue
        return super().changelist_view(request, extra_context=extra_context)

    def get_queryset(self, request):
        """
        Переопределяет метод для получения queryset заказов.

        Фильтрует заказы, возвращая только те, которые были созданы за последние 8 часов,
        что соответствует времени смены.

        Args:
            request: HTTP запрос.

        Returns:
            QuerySet: Отфильтрованный набор заказов за смену.
        """
        qs = super().get_queryset(request)
        start_of_shift = timezone.now() - timedelta(hours=8)  # Фильтрация по времени (восьмичасовая смена)
        return qs.filter(created_at__gte=start_of_shift)  # Возвращает только заказы за смену
