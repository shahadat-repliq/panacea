from django.contrib import admin
from .models import Product, ProductRequest


class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = (
        "uid",
        "title",
        "description",
        "unit_price",
        "quantity",
        "is_active",
        "type",
    )
    search_fields = ("title", "description", "is_active", "type")

    ordering = ("title",)


class ProductRequestAdmin(admin.ModelAdmin):
    model = ProductRequest
    list_display = (
        "uid",
        "product",
        "user",
        "organization",
    )
    search_fields = (
        "uid",
        "status",
    )

    ordering = ("-created_at",)


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductRequest, ProductRequestAdmin)
