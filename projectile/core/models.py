from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from .rest.managers.user_manager import UserManager
from shared.base_model import BaseUserModel


class User(AbstractBaseUser, BaseUserModel, PermissionsMixin):
    email = models.EmailField(blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = PhoneNumberField(unique=True, db_index=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "phone_number"

    objects = UserManager()

    def __str__(self):
        return str(self.phone_number)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
