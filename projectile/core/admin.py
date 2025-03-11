from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class BaseUser(UserAdmin):
    model = User
    list_display = (
        # "username",
        "email",
        "is_staff",
        "first_name",
        "last_name",
        "phone_number",
        "status",
        "role",
        "created_at",
        "last_login",
    )
    ordering = ["created_at", "first_name", "last_name", "status"]
    search_fields = ["first_name", "last_name", "phone_number", "status"]
    list_filter = ["is_staff", "status"]


admin.site.register(User, BaseUser)
