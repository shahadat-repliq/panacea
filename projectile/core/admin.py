from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class BaseUser(UserAdmin):
    model = User
    list_display = ("username", "email", "is_staff")
    ordering = ["email"]


admin.site.register(User, BaseUser)
