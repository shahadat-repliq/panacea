from django.contrib import admin
from cart.models import Cart, CartItem


class CartAdmin(admin.ModelAdmin):
    model = Cart
    list_display = ["uid", "user__uid", "user", "created_at"]
    ordering = ["-created_at"]

    # def has_delete_permission(self, request, obj=...):
    #     return False


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)
