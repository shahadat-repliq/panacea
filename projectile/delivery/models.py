from django.contrib.auth import get_user_model
from django.db import models

from address.models import Address
from order.models import Order
from shared.base_model import BaseModel

User = get_user_model()


class Delivery(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assignee = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
