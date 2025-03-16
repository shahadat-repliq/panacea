from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response

from order.models import Order
from order.rest.serializers.order import OrderSerializer, CreateOrderSerializer

User = get_user_model()


class OrderViewSet(ListAPIView, CreateAPIView):

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(
            data=request.data,
            context={"user_uid": self.request.user.uid},
        )
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateOrderSerializer
        return OrderSerializer

    def get_queryset(self):
        user_uid = self.request.user.uid
        return Order.objects.filter(user_id=user_uid)
