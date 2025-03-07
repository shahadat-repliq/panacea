"""Here is the some common serializer which used whole project wise"""

from rest_framework import serializers

from core.models import User


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
        ]
