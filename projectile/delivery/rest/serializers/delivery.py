from django.contrib.auth import get_user_model
from django.db import transaction
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from delivery.models import Delivery, DeliveryUser
from shared.choices import DeliveryStatus, UserRole
from shared.serializers import AddressSerializer

User = get_user_model()


class DeliverySerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Delivery
        fields = ["uid", "user", "assignee", "address", "delivery_status", "order"]


class DeliveryUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryUser
        fields = [
            "uid",
            "user",
            "role",
            "created_at",
        ]


class CreateDeliveryUserSerializer(serializers.Serializer):
    phone_number = PhoneNumberField(write_only=True)
    role = serializers.CharField()

    def validate_phone_number(self, value):
        user = User.objects.filter(phone_number=value).first()

        if user is None:
            raise serializers.ValidationError(
                "User doesn't exist, please check your phone number"
            )

        return value

    def create(self, validated_data):
        with transaction.atomic():
            phone_number = validated_data["phone_number"]
            role = validated_data["role"]

            user = User.objects.filter(phone_number=phone_number).first()

            if DeliveryUser.objects.filter(user=user).exists():
                raise serializers.ValidationError("Delivery user already exists")

            if role not in UserRole.values:
                raise serializers.ValidationError("Role doesn't exist")

            delivery_user = DeliveryUser.objects.create(user=user, role=role)

            return delivery_user


class DeliveryStatusSerializer(serializers.Serializer):
    delivery_status = serializers.CharField()

    def validate_delivery_status(self, value):
        if value not in DeliveryStatus.values:
            raise serializers.ValidationError("Invalid delivery status")
        return value

    def update(self, instance, validated_data):
        with transaction.atomic():
            delivery_status = validated_data.get("delivery_status")

            user = instance.assignee

            delivery_user = DeliveryUser.objects.filter(uid=user.uid).first()

            if instance.delivery_status == DeliveryStatus.COMPLETED:
                if delivery_status != DeliveryStatus.COMPLETED:
                    if delivery_user.role not in ["ADMIN", "OWNER"]:
                        raise serializers.ValidationError(
                            {
                                "detail": "Only Admin/Owner can undo a completed delivery."
                            }
                        )

            instance.delivery_status = delivery_status
            instance.save()

            return instance


class DeliveryAssignSerializer(serializers.Serializer):
    delivery_id = serializers.UUIDField(
        source="uid",
    )
    assignee = serializers.UUIDField()

    def update(self, instance, validated_data):
        assignee = validated_data.get("assignee")

        delivery_user = DeliveryUser.objects.filter(uid=assignee).first()

        if delivery_user is None:
            raise serializers.ValidationError("User not found")

        instance.assignee = delivery_user
        instance.save()

        return instance
