from django.contrib.auth import get_user_model
from django.db import models

from address.models import Address
from order.models import Order
from shared.base_model import BaseModel
from shared.choices import DeliveryStatus, UserRole

User = get_user_model()


class DeliveryUser(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    role = models.CharField(
        max_length=100, choices=UserRole.choices, default=UserRole.STAFF
    )

    def __str__(self):
        return f"{self.user.phone_number} {self.role}"


class Delivery(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="deliveries",
    )
    assignee = models.ForeignKey(
        DeliveryUser,
        on_delete=models.CASCADE,
        related_name="assigned_deliveries",
        blank=True,
        null=True,
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    delivery_status = models.TextField(
        DeliveryStatus,
        choices=DeliveryStatus.choices,
        default=DeliveryStatus.PENDING,
    )

    def __str__(self):
        return f"{self.user.phone_number} - {self.order.uid}"
