from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from django.contrib.auth import get_user_model
from cart.models import Cart, CartItem
from organization.models import OrganizationProduct
from organization.rest.serializers.organization import OrganizationProductSerializer
from product.models import Product
from shared.serializers import UserSerializer
from shared.serializers import ProductSerializer

User = get_user_model()


class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    def get_product(self, obj):
        if isinstance(obj.content_object, Product):
            return ProductSerializer(obj.content_object).data
        elif isinstance(obj.content_object, OrganizationProduct):
            return OrganizationProductSerializer(obj.content_object).data
        return None

    def get_total_price(self, cart_item):
        return cart_item.content_object.unit_price * cart_item.quantity

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
            [
                item.quantity * item.content_object.unit_price
                for item in cart.cart_items.all()
            ]
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
    product_id = serializers.UUIDField(write_only=True)

    def validate_product_id(self, value):
        if Product.objects.filter(uid=value).exists():
            self.product_type = "product"
        elif OrganizationProduct.objects.filter(uid=value).exists():
            self.product_type = "organization_product"
        else:
            raise serializers.ValidationError("Invalid product ID")
        return value

    def save(self, **kwargs):
        # Get the cart ID from the context
        cart_id = self.context.get("uid")
        product_id = self.validated_data["product_id"]
        quantity = self.validated_data["quantity"]

        if self.product_type == "product":
            product_instance = Product.objects.get(uid=product_id)
            content_type = ContentType.objects.get_for_model(Product)
            object_id = product_instance.uid  # Store the UID of the Product instance
        else:
            product_instance = OrganizationProduct.objects.get(uid=product_id)
            content_type = ContentType.objects.get_for_model(OrganizationProduct)
            object_id = product_instance.uid

        cart_item, created = CartItem.objects.update_or_create(
            cart_id=cart_id,
            content_type=content_type,
            object_id=object_id,
            defaults={"quantity": quantity},
        )

        self.instance = cart_item
        return cart_item

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
