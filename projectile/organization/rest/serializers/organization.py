from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import transaction
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from organization.models import (
    Organization,
    OrganizationUser,
    OrganizationInventory,
    OrganizationInventoryProduct,
    OrganizationProduct,
)
from product.models import Product
from shared.choices import ProductForm
from shared.validators import ProductValidation

User = get_user_model()


class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = [
            "uid",
            "name",
            "created_at",
        ]


class OrganizationDetailSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()

    def get_users(self, obj):
        organization_users = OrganizationUser.objects.select_related(
            "user", "organization"
        ).filter(organization__uid=obj.uid)

        users_data = [
            {
                "uid": org_user.user.uid,
                "email": org_user.user.email,
                "phone_number": str(org_user.user.phone_number),
                "role": org_user.role,
            }
            for org_user in organization_users
        ]

        return users_data

    class Meta:
        model = Organization
        fields = [
            "uid",
            "name",
            "users",
            "created_at",
        ]


class OrganizationUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationUser
        fields = [
            "uid",
            "user",
            "organization",
            "role",
            "created_at",
        ]


class OrganizationInventorySerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(read_only=True)

    class Meta:
        model = OrganizationInventory
        fields = ["uid", "inventory_name", "organization"]


class CreateOrganizationInventorySerializer(serializers.Serializer):
    inventory_name = serializers.CharField()

    def create(self, validated_data):
        with transaction.atomic():
            organization = self.context.get("organization")
            inventory_name = validated_data["inventory_name"]

            return OrganizationInventory.objects.create(
                organization_id=organization, inventory_name=inventory_name
            )


class SimpleOrganizationProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ["uid", "name", "status"]


class OrganizationInventoryProductSerializer(serializers.ModelSerializer):
    uid = serializers.UUIDField(source="product.uid", read_only=True)
    title = serializers.CharField(source="product.title")
    description = serializers.CharField(source="product.description")
    image = serializers.ImageField(
        source="product.image", required=False, allow_null=True
    )
    unit_price = serializers.DecimalField(
        source="product.unit_price",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(1)],
    )
    quantity = serializers.IntegerField(
        source="product.quantity", validators=[MinValueValidator(1)]
    )
    type = serializers.ChoiceField(source="product.type", choices=ProductForm.choices)
    is_active = serializers.BooleanField(source="product.is_active", default=True)
    organization = SimpleOrganizationProductSerializer(
        source="product.organization", read_only=True
    )

    class Meta:
        model = OrganizationInventoryProduct
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

    def create(self, validated_data):
        with transaction.atomic():
            product_data = validated_data.pop("product")
            organization = self.context.get("organization")

            product = OrganizationProduct.objects.create(
                **product_data, organization_id=organization
            )

            organization_inventory_product = (
                OrganizationInventoryProduct.objects.create(
                    product=product, **validated_data
                )
            )

            return organization_inventory_product


class CreateOrganizationSerializer(serializers.Serializer):
    phone_number = PhoneNumberField(write_only=True)
    name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate_phone_number(self, value):
        user = User.objects.filter(phone_number=value).first()

        if (
            user
            and OrganizationUser.objects.select_related(
                "organization",
                "user",
            )
            .filter(user=user)
            .exists()
        ):
            raise serializers.ValidationError(
                "This phone number is already in use by another organization."
            )

        return value

    def create(self, validated_data):
        with transaction.atomic():
            phone_number = validated_data["phone_number"]
            name = validated_data["name"]
            password = validated_data["password"]

            user, created = User.objects.get_or_create(
                phone_number=phone_number,
                defaults={"password": make_password(password)},
            )

            organization = Organization.objects.prefetch_related("users").create(
                name=name
            )

            organization_user = OrganizationUser.objects.select_related(
                "organization", "user"
            ).create(organization=organization, user=user, role="OWNER")

            OrganizationInventory.objects.create(
                organization=organization, inventory_name="Default Inventory"
            )

            return organization_user


class OrganizationProductSerializer(serializers.ModelSerializer):

    def get_product(self, obj):
        if isinstance(obj, Product):
            return {
                "uid": obj.uid,
                "title": obj.title,
                "description": obj.description,
                "image": obj.image.url if obj.image else None,
                "unit_price": obj.unit_price,
                "quantity": obj.quantity,
                "type": obj.type,
                "is_active": obj.is_active,
                "organization": obj.organization.uid if obj.organization else None,
            }
        elif isinstance(obj, OrganizationProduct):
            return {
                "uid": obj.uid,
                "title": obj.title,
                "description": obj.description,
                "image": obj.image.url if obj.image else None,
                "unit_price": obj.unit_price,
                "quantity": obj.quantity,
                "type": obj.type,
                "is_active": obj.is_active,
                "organization": obj.organization.uid,
            }

    def to_representation(self, instance):
        product_data = self.get_product(instance)
        return product_data


class OrganizationInventoryDetailSerializer(serializers.ModelSerializer):
    products = OrganizationInventoryProductSerializer(read_only=True, many=True)

    class Meta:
        model = OrganizationInventory
        fields = ["uid", "inventory_name", "organization", "products"]


class OrganizationInventoryProductDetailSerializer(serializers.ModelSerializer):
    uid = serializers.UUIDField(source="product.uid", read_only=True)
    title = serializers.CharField(source="product.title")
    description = serializers.CharField(source="product.description")
    image = serializers.ImageField(
        source="product.image", required=False, allow_null=True
    )
    unit_price = serializers.DecimalField(
        source="product.unit_price",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(1)],
    )
    quantity = serializers.IntegerField(
        source="product.quantity", validators=[MinValueValidator(1)]
    )
    type = serializers.ChoiceField(source="product.type", choices=ProductForm.choices)
    is_active = serializers.BooleanField(
        source="product.is_active",
    )

    class Meta:
        model = OrganizationInventoryProduct
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

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Remove 'uid' during PATCH
        if self.context.get("request") and self.context["request"].method == "PATCH":
            representation.pop("uid", None)

        return representation

    def update(self, instance, validated_data):

        with transaction.atomic():
            product_data = validated_data.pop("product", {})

            for attr, value in validated_data.items():
                setattr(instance, attr, value)

            for attr, value in product_data.items():
                setattr(instance.product, attr, value)

            instance.product.save()

            instance.save()

            return instance
