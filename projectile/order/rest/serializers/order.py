from django.db import transaction
from rest_framework import serializers

from address.models import Address
from cart.models import Cart, CartItem
from delivery.models import Delivery
from order.models import Order, OrderItem
from organization.models import OrganizationProduct
from organization.rest.serializers.organization import OrganizationProductSerializer
from product.models import Product
from shared.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, order_items):
        return order_items.quantity * order_items.unit_price

    class Meta:
        model = OrderItem
        fields = ["uid", "product", "unit_price", "quantity", "total_price"]

    def get_product(self, obj):
        if isinstance(obj.content_object, Product):
            return ProductSerializer(obj.content_object).data
        elif isinstance(obj.content_object, OrganizationProduct):
            return OrganizationProductSerializer(obj.content_object).data
        return None


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, order):
        return sum(
            [item.quantity * item.unit_price for item in order.order_items.all()]
        )

    class Meta:
        model = Order
        fields = ["uid", "order_items", "total_price"]


class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, value):
        user_id = self.context["user_uid"]

        try:
            cart = (
                Cart.objects.prefetch_related("cart_items", "cart_items__content_type")
                .select_related("user")
                .get(user_id=user_id, uid=value)
            )
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

            cart_items = CartItem.objects.filter(cart_id=cart_id)
            if not cart_items.exists():
                raise serializers.ValidationError({"detail": "Cart is empty."})

            address = Address.objects.filter(user__uid=user_id).first()
            if not address:
                raise serializers.ValidationError(
                    {"detail": "Need to create address first to order."}
                )

            order_items = [
                OrderItem(
                    order=order,
                    content_type=item.content_type,
                    object_id=item.object_id,
                    unit_price=item.content_object.unit_price,
                    quantity=item.quantity,
                )
                for item in cart_items
                if isinstance(item.content_object, (Product, OrganizationProduct))
            ]

            OrderItem.objects.bulk_create(order_items)
            cart_items.delete()

            user = order.user

            Delivery.objects.select_related(
                "order", "user", "address"
            ).create(
                user=user,
                order=order,
                address=address,
            )

            return order
