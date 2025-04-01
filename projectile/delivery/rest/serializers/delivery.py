from rest_framework import serializers

from delivery.models import Delivery


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ["user", "assignee", "address", "delivery_status", "order"]
