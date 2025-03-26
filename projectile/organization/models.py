from django.contrib.auth import get_user_model
from django.db import models


from shared.base_model import BaseModel
from shared.choices import UserRole

User = get_user_model()


class Organization(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


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
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.inventory_name} {self.pk}"


class OrganizationInventoryProduct(BaseModel):
    organization_inventory = models.ForeignKey(
        OrganizationInventory, on_delete=models.CASCADE
    )
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.organization_inventory.inventory_name}"
