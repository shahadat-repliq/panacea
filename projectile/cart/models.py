import uuid

from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth import get_user_model

from product.models import Product

from shared.base_model import BaseUserModel

User = get_user_model()


class Cart(BaseUserModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class CartItem(BaseUserModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        unique_together = [["cart", "product"]]
