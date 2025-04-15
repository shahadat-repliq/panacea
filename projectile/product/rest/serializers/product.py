from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from organization.models import OrganizationUser, OrganizationProduct
from organization.rest.serializers.organization import OrganizationSerializer
from product.models import Product, ProductRequest
from shared.choices import ProductRequestStatus


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = fields = [
            "uid",
            "title",
            "description",
            "image",
            "unit_price",
            "quantity",
            "type",
            "is_active",
        ]


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
            "organization",
        ]


class AddProductRequestSerializer(serializers.Serializer):
    product_id = serializers.UUIDField(source="uid", write_only=True)

    def validate_product_id(self, value):
        if ProductRequest.objects.filter(product__uid=value).exists():
            raise serializers.ValidationError(
                {"detail": "You have already requested this product."}
            )
        return value

    def create(self, validated_data):
        user = self.context["user"]

        try:
            org_user = OrganizationUser.objects.get(user=user)
        except OrganizationUser.DoesNotExist:
            raise serializers.ValidationError({"detail": "Invalid organization user."})

        try:
            product = OrganizationProduct.objects.get(uid=validated_data["uid"])
        except OrganizationProduct.DoesNotExist:
            raise serializers.ValidationError({"detail": "Product does not exist."})

        if product.organization != org_user.organization:
            raise serializers.ValidationError(
                {"detail": "This product does not belong to your organization."}
            )

        return ProductRequest.objects.create(
            product=product, user=org_user, organization=org_user.organization
        )


class ProductRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductRequest
        fields = ["uid", "product", "user", "organization", "status"]


class ProductRequestDetailSerializer(serializers.Serializer):
    status = serializers.CharField()

    uid = serializers.UUIDField(read_only=True)
    product = serializers.SerializerMethodField()
    organization = serializers.SerializerMethodField()

    def validate_status(self, value):
        if value not in ProductRequestStatus.values:
            raise ValidationError({"detail": "Invalid status."})
        return value

    def get_product(self, obj):
        return SimpleProductSerializer(obj.product).data

    def get_organization(self, obj):
        return OrganizationSerializer(obj.organization).data

    def to_representation(self, instance):
        request = self.context.get("request")
        if request and request.method.lower() in ["patch", "put"]:
            return {
                "status": instance.status,
            }

        return {
            "uid": str(instance.uid),
            "product": self.get_product(instance),
            "organization": self.get_organization(instance),
            "status": instance.status,
        }

    def update(self, instance, validated_data):
        new_status = validated_data.get("status")

        if (
            instance.status == ProductRequestStatus.APPROVED
            and new_status == ProductRequestStatus.APPROVED
        ):
            raise ValidationError({"detail": "Product has already been approved."})

        with transaction.atomic():
            if new_status == ProductRequestStatus.APPROVED:
                org_product = instance.product

                Product.objects.create(
                    title=org_product.title,
                    description=org_product.description,
                    image=org_product.image,
                    unit_price=org_product.unit_price,
                    quantity=org_product.quantity,
                    type=org_product.type,
                    is_active=True,
                    organization=None,
                    is_custom=False,
                )

            instance.status = new_status
            instance.save()

        return instance
