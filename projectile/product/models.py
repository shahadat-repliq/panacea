import uuid
from django.db import models

from shared.base_model import BaseProductModel


class ProductForm(models.TextChoices):
    TABLETS = "TABLETS", "Tablets"
    SYRUP = "SYRUP", "Syrup"
    INJECTION = "INJECTION", "Injection"
    OINTMENT = "OINTMENT", "Ointment"
    CAPSULE = "CAPSULE", "Capsule"
    DEFAULT = "NONE", "None"


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

    def __str__(self):
        return self.title
