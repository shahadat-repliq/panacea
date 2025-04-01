from rest_framework import viewsets
from rest_framework.generics import ListAPIView

from delivery.models import Delivery
from delivery.rest.serializers.delivery import DeliverySerializer


class DeliveryViewSet(ListAPIView):
    serializer_class = DeliverySerializer

    def get_queryset(self):
        return Delivery.objects.filter(user=self.request.user)
