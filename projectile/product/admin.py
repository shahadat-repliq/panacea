from django.contrib import admin
from .models import Product


class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ("uid", "title", "description", "unit_price", "is_active", "type")
    search_fields = ("title", "description", "is_active", "type")

    ordering = ("title",)


admin.site.register(Product, ProductAdmin)
