from rest_framework import serializers
from django.contrib.auth import get_user_model
from cart.models import Cart, CartItem
from product.models import Product
from shared.serializers import UserSerializer

User = get_user_model()


class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "uid",
            "title",
            "unit_price",
            "quantity",
        ]


class CartItemSerializer(serializers.ModelSerializer):
    product = CartProductSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart_item):
        return cart_item.product.unit_price * cart_item.quantity

    class Meta:
        model = CartItem
        fields = [
            "uid",
            "cart",
            "product",
            "quantity",
            "total_price",
        ]


class CartSerializer(serializers.ModelSerializer):
    uid = serializers.UUIDField(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = [
            "uid",
            "user",
        ]


class CartDetailSerializer(serializers.ModelSerializer):
    uid = serializers.UUIDField(read_only=True)
    # user = UserSerializer(read_only=True)
    cart_items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    total_count = serializers.IntegerField(read_only=True)

    def get_total_price(self, cart):
        return sum(
            [item.quantity * item.product.unit_price for item in cart.cart_items.all()]
        )

    class Meta:
        model = Cart
        fields = [
            "uid",
            # "user",
            "cart_items",
            "total_count",
            "total_price",
        ]


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.UUIDField()

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError("Invalid product ID")
        return value

    def save(self, **kwargs):
        cart_id = self.context.get("uid")
        product_id = self.validated_data["product_id"]
        quantity = self.validated_data["quantity"]

        try:
            cart_items = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_items.quantity = quantity
            cart_items.save()
            self.instance = cart_items
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(
                cart_id=cart_id, **self.validated_data
            )
        return self.instance

    class Meta:
        model = CartItem
        fields = [
            "product_id",
            "quantity",
        ]


class UpdateCartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = ["quantity"]
