from django.contrib.auth import get_user_model
from django.db import transaction
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.response import Response

from organization.models import (
    Organization,
    OrganizationUser,
    OrganizationInventory,
    OrganizationInventoryProduct,
)
from shared.serializers import UserSerializer

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
        organization_users = OrganizationUser.objects.select_related("user").filter(
            organization__uid=obj.uid
        )

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
    class Meta:
        model = OrganizationInventory
        fields = ["uid", "organization"]


class OrganizationInventoryProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationInventoryProduct
        fields = [
            "uid",
            "product",
            "organization_inventory",
            "created_at",
        ]


class CreateOrganizationSerializer(serializers.Serializer):
    phone_number = PhoneNumberField(write_only=True)
    name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate_phone_number(self, value):
        # First, get the user with the given phone number
        user = User.objects.filter(phone_number=value).first()

        # Check if the user exists and if they are already part of an organization
        if (
            user
            and OrganizationUser.objects.select_related("organization", "user")
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
                defaults={"password": password},
            )

            organization = Organization.objects.prefetch_related("users").create(
                name=name
            )

            organization_user = OrganizationUser.objects.select_related(
                "organization"
            ).create(organization=organization, user=user, role="OWNER")

            OrganizationInventory.objects.create(organization=organization)

            return organization_user
