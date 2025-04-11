from django.db.models import Sum, Prefetch
from django.db.models.functions import Coalesce

from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateAPIView,
    ListAPIView,
    RetrieveAPIView,
    DestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from cart.models import Cart, CartItem
from cart.rest.serializers.cart import (
    CartSerializer,
    CartDetailSerializer,
    CartItemSerializer,
    AddCartItemSerializer,
    UpdateCartItemSerializer,
)


class CartViewSet(ListAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get_queryset(self):
        queryset = Cart.objects.prefetch_related("user").filter(user=self.request.user)
        return queryset


class CartDetailViewSet(RetrieveAPIView):
    serializer_class = CartDetailSerializer
    lookup_field = "uid"

    def get_queryset(self):
        cart_id = self.kwargs["uid"]
        cart_items_prefetch = Prefetch(
            "cart_items",
            queryset=CartItem.objects.select_related("content_type").prefetch_related(
                "content_object",
            ),
        )
        queryset = (
            Cart.objects.select_related("user")
            .prefetch_related(cart_items_prefetch)
            .filter(uid=cart_id, user=self.request.user)
            .annotate(total_count=Coalesce(Sum("cart_items__quantity"), 0))
        )
        return queryset


class CartItemViewSet(ListAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView):

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {"uid": self.kwargs["uid"]}

    def get_queryset(self):
        cart_id = self.kwargs["uid"]
        return CartItem.objects.filter(
            cart_id=cart_id,
        )

    def destroy(self, request, *args, **kwargs):
        cart_id = self.kwargs["uid"]

        cart_items = CartItem.objects.filter(cart_id=cart_id)

        if not cart_items.exists():
            return Response(
                {"detail": "No items in the cart."},
                status=status.HTTP_404_NOT_FOUND,
            )

        cart_items.delete()

        return Response(
            {"message": "Cart items have been cleared."},
            status=status.HTTP_204_NO_CONTENT,
        )


class CartItemDetailViewSet(RetrieveUpdateAPIView, DestroyAPIView):
    http_method_names = ["get", "patch", "delete"]

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_queryset(self):
        cart_id = self.kwargs["uid"]
        cart_item_id = self.kwargs["pk"]

        queryset = (
            CartItem.objects.select_related("content_type", "cart")
            .prefetch_related("content_object")
            .filter(cart_id=cart_id, uid=cart_item_id)
        )

        return queryset
