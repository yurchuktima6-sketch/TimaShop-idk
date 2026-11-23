from decimal import Decimal
from django.conf import settings
from django.db import models
from shop.models import Product


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Очікує на обробку'),
        ('paid', 'Оплачено'),
        ('shipped', 'Відправлено'),
        ('delivered', 'Доставлено'),
        ('cancelled', 'Скасовано'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders',
        verbose_name='Користувач'
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name='Створено')
    updated = models.DateTimeField(auto_now=True, verbose_name='Оновлено')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Статус замовлення'
    )
    paid = models.BooleanField(default=False, verbose_name='Оплачено')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'

    def __str__(self):
        return f'Замовлення #{self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE,
        verbose_name='Замовлення'
    )
    product = models.ForeignKey(
        Product,
        related_name='order_items',
        on_delete=models.CASCADE,
        verbose_name='Товар (Гра)'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ціна')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Кількість')

    def __str__(self):
        return f'{self.id}'

    def get_cost(self):
        return self.price * self.quantity


class ShippingAddress(models.Model):
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='shipping_address',
        verbose_name='Замовлення'
    )
    full_name = models.CharField(max_length=100, verbose_name="Ім'я та прізвище")
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    city = models.CharField(max_length=100, verbose_name='Місто')
    address = models.CharField(max_length=250, verbose_name='Адреса / Відділення Нової Пошти')
    postal_code = models.CharField(max_length=20, verbose_name='Поштовий індекс')

    class Meta:
        verbose_name = 'Адреса доставки'
        verbose_name_plural = 'Адреси доставки'

    def __str__(self):
        return f'Адреса для замовлення #{self.order.id}'