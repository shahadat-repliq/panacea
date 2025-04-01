from django.contrib.auth import get_user_model
from django.db import models

from shared.base_model import BaseModel, BaseProductModel
from shared.choices import UserRole, ProductForm

User = get_user_model()


class Organization(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class OrganizationProduct(BaseProductModel):
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
        Organization,
        on_delete=models.CASCADE,
    )
    is_custom = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class OrganizationUser(BaseModel):
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="users"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=100, choices=UserRole.choices, default=UserRole.OWNER
    )

    class Meta:
        unique_together = [["organization", "user"]]

    def __str__(self):
        return f"{self.user.phone_number} {self.organization.name} {self.role}"


class OrganizationInventory(BaseModel):
    inventory_name = models.CharField(max_length=100)
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="inventories"
    )

    def __str__(self):
        return f"{self.inventory_name} {self.pk}"


class OrganizationInventoryProduct(BaseModel):
    organization_inventory = models.ForeignKey(
        OrganizationInventory, on_delete=models.CASCADE, related_name="products"
    )
    product = models.ForeignKey(OrganizationProduct, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.organization_inventory.inventory_name}"
