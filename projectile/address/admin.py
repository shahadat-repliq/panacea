from django.contrib import admin

from address.models import Address


class AddressAdmin(admin.ModelAdmin):
    model = Address
    list_display = [
        "user",
        "street_address",
        "city",
        "state",
        "country",
        "is_primary_address",
    ]
    search_fields = ["city", "state", "country"]


admin.site.register(Address, AddressAdmin)
