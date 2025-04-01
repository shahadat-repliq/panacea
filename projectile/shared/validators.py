from django.core.exceptions import ValidationError
from rest_framework import serializers

from shared.choices import ProductForm


class ProductValidation:

    @staticmethod
    def validate_title(value):
        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        if len(value) > 255:
            raise serializers.ValidationError(
                "Title cannot be more than 255 characters."
            )
        return value

    @staticmethod
    def validate_description(value):
        if not value.strip():
            raise serializers.ValidationError("Description cannot be empty.")
        return value

    @staticmethod
    def validate_image(value):
        """Optional: Validate image format (if needed)."""
        if value and value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("Image size must be less than 5 MB.")
        if value and not value.name.lower().endswith(("jpg", "jpeg", "png")):
            raise serializers.ValidationError(
                "Image must be in JPG, JPEG, or PNG format."
            )
        return value

    @staticmethod
    def validate_type(value):
        valid_types = [choice[0] for choice in ProductForm.choices]
        if value not in valid_types:
            raise serializers.ValidationError(
                f"Invalid product type. Valid choices are: {', '.join(valid_types)}"
            )
        return value
