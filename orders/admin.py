from django.contrib import admin
from .models import Order, OrderItem


class ItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'product_name', 'price', 'quantity')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total', 'city', 'created_at')
    list_filter = ('city', 'created_at')
    inlines = [ItemInline]
