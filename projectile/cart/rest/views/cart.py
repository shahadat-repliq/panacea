from django.db.models import Sum

from rest_framework.exceptions import NotFound
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from cart.models import Cart
from cart.rest.serializers.cart import CartSerializer, UserCartSerializer


class CartViewSet(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserCartSerializer

    def get_object(self):
        user = self.request.user
        try:
            return (
                Cart.objects.select_related("user")
                .prefetch_related("cart_items")
                .annotate(
                    total_quantity=Sum("cart_items__quantity"),
                )
                .get(user=user)
            )

        except Cart.DoesNotExist:
            raise NotFound(detail="Cart not found")
