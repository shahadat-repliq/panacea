from rest_framework import viewsets
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated

from address.models import Address
from address.rest.serializers.address import CreateAddressSerializer
from shared.serializers import AddressSerializer


class AddressViewSet(ListAPIView, CreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {"user": self.request.user}

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateAddressSerializer
        return AddressSerializer

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
