from rest_framework import status
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from organization.permissions import (
    IsBaseOrganizationOwnerOrAdmin,
)
from product.models import Product, ProductRequest
from product.rest.serializers.product import (
    ProductSerializer,
    AddProductRequestSerializer,
    ProductRequestSerializer,
    ProductRequestDetailSerializer,
)


class ProductViewSet(ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return Product.objects.all().order_by("-created_at")


class AddProductRequestViewSet(CreateAPIView):
    serializer_class = AddProductRequestSerializer
    permission_classes = [IsAuthenticated, IsBaseOrganizationOwnerOrAdmin]

    def get_serializer_context(self):
        return {"user": self.request.user}

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_request = serializer.save()

        return Response(
            {
                "message": "Product request submitted successfully.",
                "product_request_id": str(product_request.uid),
                "product": product_request.product.title,
            },
            status=status.HTTP_201_CREATED,
        )


class ProductRequestViewSet(ListAPIView):
    serializer_class = ProductRequestSerializer
    permission_classes = [IsAuthenticated, IsBaseOrganizationOwnerOrAdmin]

    def get_queryset(self):
        return (
            ProductRequest.objects.select_related(
                "user",
                "organization",
                "product",
            )
            .all()
            .order_by("-created_at")
        )


class ProductRequestDetailViewSet(RetrieveAPIView, UpdateAPIView):
    serializer_class = ProductRequestDetailSerializer
    http_method_names = ["get", "patch"]

    def get_object(self):
        return ProductRequest.objects.select_related(
            "user",
            "organization",
            "product",
        ).get(uid=self.kwargs["product_id"])
