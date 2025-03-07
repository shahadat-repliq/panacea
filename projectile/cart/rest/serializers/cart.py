from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.db.models import Sum

from cart.models import Cart, CartItem
from cart.choices import CartActionchoices

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
    # total_price = serializers.SerializerMethodField()

    # def get_total_price(self, cart_item):
    #     return cart_item.product.unit_price * cart_item.quantity

    class Meta:
        model = CartItem
        fields = [
            "uid",
            "product",
            "quantity",
            "created_at",
            "updated_at",
        ]


class CartSerializer(serializers.ModelSerializer):
    uid = serializers.CharField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
    )
    cart_items = CartItemSerializer(many=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart):
        return sum(
            [item.quantity * item.product.unit_price for item in cart.cart_items.all()]
        )

    class Meta:
        model = Cart
        fields = ["uid", "user", "cart_items", "total_price"]

    def create(self, validated_data):
        request = self.context.get("request")
        if "user" not in validated_data:
            if request and request.user.is_authenticated():
                validated_data["user"] = request.user

        return Cart.objects.create(**validated_data)


class UserCartSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    cart_items = CartItemSerializer(many=True, read_only=True)
    total_quantity = serializers.IntegerField(read_only=True)
    total_price = serializers.SerializerMethodField()
    product_uid = serializers.UUIDField(write_only=True)
    quantity = serializers.IntegerField(write_only=True, default=1)
    action_choices = serializers.ChoiceField(
        choices=CartActionchoices, default=CartActionchoices.ADD
    )

    class Meta:
        model = Cart
        fields = [
            "uid",
            "user",
            "cart_items",
            "total_quantity",
            "product_uid",
            "quantity",
            "total_price",
            "action_choices",
            "updated_at",
        ]
        read_only_fields = [
            "uid",
            "user",
            "created_at",
            "updated_at",
        ]

    def get_total_price(self, obj):
        if obj.cart_items.exists():
            total_price = 0
            for item in obj.cart_items.all():
                total_price += item.quantity * item.product.unit_price
            return total_price

    def update(self, instance, validated_data):
        user = self.context.get("request").user
        product_uid = validated_data.get("product_uid")
        quantity = validated_data.get("quantity")
        action_choices = validated_data.get("action_choices")

        try:
            product = Product.objects.get(uid=product_uid)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product not found")

        # Create cart item
        cart_items, created = CartItem.objects.get_or_create(
            cart=user.cart, product=product
        )

        if action_choices == CartActionchoices.ADD:
            cart_items.quantity = quantity
            cart_items.save()
        else:
            cart_items.delete()

        return instance
