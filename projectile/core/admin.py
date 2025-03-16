from django.contrib import admin
from .models import User


class BaseUser(admin.ModelAdmin):
    model = User
    list_display = (
        # "username",
        "uid",
        "email",
        "is_staff",
        "first_name",
        "last_name",
        "phone_number",
        "status",
        "role",
        "created_at",
    )
    ordering = ["created_at", "first_name", "last_name", "status"]
    search_fields = ["first_name", "last_name", "phone_number", "status"]
    list_filter = ["is_staff", "status"]
    list_display_links = ["uid"]


admin.site.register(User, BaseUser)
