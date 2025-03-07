from django.db.models.signals import post_save
from django.dispatch import receiver

from cart.models import Cart
from core.models import User


@receiver(post_save, sender=User)
def create_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.get_or_create(user=instance)
