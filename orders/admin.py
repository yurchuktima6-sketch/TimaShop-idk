from django.contrib import admin
from .models import Order, OrderItem, ShippingAddress


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0


class ShippingAddressInline(admin.StackedInline):
    model = ShippingAddress
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'paid', 'created', 'get_total_cost']
    list_filter = ['paid', 'status', 'created']
    inlines = [ShippingAddressInline, OrderItemInline]