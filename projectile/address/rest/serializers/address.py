from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers, status
from rest_framework.response import Response

from address.models import Address


class CreateAddressSerializer(serializers.Serializer):
    user = PhoneNumberField()
    street_address = serializers.CharField(max_length=255)
    city = serializers.CharField(max_length=255)
    state = serializers.CharField(max_length=255)
    postal_code = serializers.CharField(max_length=255)
    country = serializers.CharField(max_length=255)
    is_primary_address = serializers.BooleanField(default=False)

    def validate_user(self, value):
        request_user = self.context["user"]
        if value != request_user.phone_number:
            raise serializers.ValidationError(
                "Your phone number does not match the one associated with your account."
            )

        return value

    def create(self, validated_data):
        request_user = self.context["user"]

        address = Address.objects.create(
            user=request_user,
            street_address=validated_data["street_address"],
            city=validated_data["city"],
            state=validated_data["state"],
            postal_code=validated_data["postal_code"],
            country=validated_data["country"],
            is_primary_address=validated_data["is_primary_address"],
        )

        return address

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
