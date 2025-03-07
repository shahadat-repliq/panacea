from rest_framework import serializers
from product.models import Product


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            "uid",
            "title",
            "description",
            "image",
            "unit_price",
            "quantity",
            "type",
            "is_active",
        ]
