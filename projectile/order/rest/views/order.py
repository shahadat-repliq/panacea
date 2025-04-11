from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db.models import Prefetch
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response

from order.models import Order, OrderItem
from order.rest.serializers.order import OrderSerializer, CreateOrderSerializer
from organization.models import OrganizationProduct
from product.models import Product

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

        # Prefetch related order_items with content_object (Product or OrganizationProduct)
        order_items_prefetch = Prefetch(
            "order_items",
            queryset=OrderItem.objects.select_related("content_type").prefetch_related(
                "content_object",
            ),
        )

        return (
            Order.objects.select_related("user")
            .prefetch_related(order_items_prefetch)
            .filter(user_id=user_uid)
            .order_by("-created_at")
        )
