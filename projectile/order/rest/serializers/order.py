from django.db import transaction
from rest_framework import serializers

from cart.models import Cart, CartItem
from order.models import Order, OrderItem
from shared.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ["uid", "product", "unit_price", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "uid",
            "order_items",
        ]


class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, value):
        user_id = self.context["user_uid"]

        try:
            cart = Cart.objects.get(user_id=user_id, uid=value)
        except Cart.DoesNotExist:
            raise serializers.ValidationError(
                "Cart does not exist or does not belong to you."
            )
        return value

    def save(self):
        with transaction.atomic():
            cart_id = self.validated_data["cart_id"]
            user_id = self.context["user_uid"]

            order = Order.objects.create(user_id=user_id)

            cart_items = CartItem.objects.select_related("product").filter(
                cart_id=cart_id
            )
            if not cart_items.exists():
                raise serializers.ValidationError({"detail": "Cart is empty."})

            order_items = [
                OrderItem(
                    order=order,
                    product=item.product,
                    unit_price=item.product.unit_price,
                    quantity=item.quantity,
                )
                for item in cart_items
            ]

            OrderItem.objects.bulk_create(order_items)
            cart_items.delete()
            return order
