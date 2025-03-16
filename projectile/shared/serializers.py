from rest_framework import serializers

from core.models import User
from product.models import Product


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "uid",
            "email",
            "first_name",
            "last_name",
            "phone_number",
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
