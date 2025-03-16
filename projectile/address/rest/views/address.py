from rest_framework import viewsets
from rest_framework.generics import ListAPIView

from address.models import Address
from address.rest.serializers.address import AddressSerializer


class AddressViewSet(ListAPIView):
    serializer_class = AddressSerializer

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
