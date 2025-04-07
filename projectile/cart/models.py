import uuid

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
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
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey("content_type", "object_id")
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        unique_together = [["cart", "content_type", "object_id"]]
