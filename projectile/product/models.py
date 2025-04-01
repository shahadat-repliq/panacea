import uuid
from django.db import models

from organization.models import Organization
from shared.base_model import BaseProductModel
from shared.choices import ProductForm


class Product(BaseProductModel):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    type = models.CharField(
        max_length=10, choices=ProductForm.choices, default=ProductForm.DEFAULT
    )
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, blank=True, null=True
    )
    is_custom = models.BooleanField(default=False)

    def __str__(self):
        return self.title
