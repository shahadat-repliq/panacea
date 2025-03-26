from django.contrib import admin

from order.models import Order, OrderItem


class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ["uid", "created_at", "user"]


class OrderItemAdmin(admin.ModelAdmin):
    model = OrderItem
    list_display = [
        "uid",
    ]


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
