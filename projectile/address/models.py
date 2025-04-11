from django.contrib.auth import get_user_model
from django.db import models

from shared.base_model import BaseModel

User = get_user_model()


class Address(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    street_address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    is_primary_address = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.street_address}, {self.city}, {self.state}, {self.country}"

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"
