from rest_framework import serializers

from address.models import Address
from core.models import User
from product.models import Product


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "user",
            "street_address",
            "city",
            "state",
            "country",
            "is_primary_address",
        ]


class UserSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            "uid",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "addresses",
            "last_login",
            "created_at",
            "updated_at",
            "role",
        ]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "uid",
            "title",
            "unit_price",
            "quantity",
        ]
