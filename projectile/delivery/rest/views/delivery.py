from rest_framework import viewsets, status
from rest_framework.exceptions import NotFound
from rest_framework.generics import (
    ListAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    CreateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from delivery.models import Delivery, DeliveryUser
from delivery.rest.serializers.delivery import (
    DeliverySerializer,
    DeliveryAssignSerializer,
    DeliveryStatusSerializer,
    DeliveryUserSerializer,
    CreateDeliveryUserSerializer,
)
from shared.permissions import IsDeliveryUser


class DeliveryViewSet(ListAPIView, RetrieveAPIView):
    serializer_class = DeliverySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Delivery.objects.filter(user=self.request.user)


class DeliveryUserViewSet(ListAPIView):
    serializer_class = DeliveryUserSerializer

    queryset = DeliveryUser.objects.all()
    permission_classes = [IsAuthenticated]


class CreateDeliveryUserViewSet(CreateAPIView):
    serializer_class = CreateDeliveryUserSerializer
    permission_classes = [IsAuthenticated]
    queryset = DeliveryUser.objects.all()


class DeliveryDetailViewSet(RetrieveAPIView, UpdateAPIView):
    permission_classes = [IsAuthenticated, IsDeliveryUser]
    http_method_names = ["get", "patch", "delete"]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return DeliverySerializer
        elif self.request.method == "PATCH":
            return DeliveryStatusSerializer

    def get_serializer_context(self):
        return {"user": self.request.user}

    def get_object(self):
        delivery_id = self.kwargs.get("delivery_id")
        try:
            delivery = Delivery.objects.get(
                uid=delivery_id,
            )
        except Delivery.DoesNotExist:
            raise NotFound(
                "Delivery not found or you do not have access to this delivery"
            )

        return delivery


class DeliveryAssignViewSet(UpdateAPIView):
    serializer_class = DeliveryAssignSerializer
    http_method_names = ["patch"]
    permission_classes = [IsAuthenticated]
    queryset = Delivery.objects.all()

    def get_object(self):
        delivery_id = self.request.data.get("delivery_id")

        try:
            delivery = Delivery.objects.get(uid=delivery_id)
        except Delivery.DoesNotExist:
            raise NotFound("Delivery not found with the provided ID")

        return delivery

    def patch(self, request, *args, **kwargs):
        delivery = self.get_object()
        serializer = self.get_serializer(delivery, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Delivery Assigned successfully!"}, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
