from rest_framework import viewsets
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    get_object_or_404,
    DestroyAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from organization.models import (
    Organization,
    OrganizationInventory,
    OrganizationUser,
    OrganizationInventoryProduct,
)
from organization.permissions import IsOrganizationOwnerOrAdmin
from organization.rest.serializers.organization import (
    OrganizationSerializer,
    CreateOrganizationSerializer,
    OrganizationDetailSerializer,
    OrganizationInventorySerializer,
    CreateOrganizationInventorySerializer,
    OrganizationProductSerializer,
    OrganizationInventoryDetailSerializer,
    OrganizationInventoryProductSerializer,
    OrganizationInventoryProductDetailSerializer,
    SimpleOrganizationProductSerializer,
)

from rest_framework.exceptions import NotFound, PermissionDenied, MethodNotAllowed

from product.models import Product
from product.rest.serializers.product import ProductSerializer
from django.db.models import Q


class OrganizationViewSet(ListAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Organization.objects.all()
        return Organization.objects.prefetch_related("users", "users__user").filter(
            users__user__uid=self.request.user.uid
        )


class OrganizationDetailViewSet(RetrieveAPIView):
    serializer_class = OrganizationDetailSerializer

    def get_object(self):
        org_id = self.kwargs.get("org_id")
        user = self.request.user.uid

        try:
            organization = Organization.objects.get(uid=org_id)
        except Organization.DoesNotExist:
            raise NotFound("Organization not found.")

        if not organization.users.filter(user__uid=user).exists():
            raise PermissionDenied("You are not a member of this organization.")

        return organization


class CreateOrganizationViewSet(CreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = CreateOrganizationSerializer


class OrganizationInventoryViewSet(ListAPIView):
    serializer_class = OrganizationInventorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user.uid

        org_id = self.kwargs.get("org_id")
        try:
            org = Organization.objects.get(uid=org_id)
        except Organization.DoesNotExist:
            raise NotFound("Organization not found.")

        if self.request.user.is_superuser:
            return OrganizationInventory.objects.select_related("organization").all()

        is_user_part_of_org = (
            OrganizationUser.objects.select_related(
                "organization",
                "user",
            )
            .filter(organization__uid=org.uid, user__uid=user)
            .exists()
        )

        if not is_user_part_of_org:
            raise NotFound("User is not part of this organization.")

        queryset = OrganizationInventory.objects.select_related(
            "organization",
        ).filter(organization__uid=org_id)

        return queryset


class CreateOrganizationInventoryViewSet(CreateAPIView):
    queryset = OrganizationInventory.objects.all()
    serializer_class = CreateOrganizationInventorySerializer

    def get_serializer_context(self):
        return {"organization": self.kwargs.get("org_id")}

    def perform_create(self, serializer):
        org_id = self.kwargs.get("org_id")
        user = self.request.user.uid

        try:
            organization = Organization.objects.get(pk=org_id)
        except Organization.DoesNotExist:
            raise NotFound("Organization not found.")

        if not organization.users.filter(uid=user).exists():
            raise PermissionDenied("You are not part of this organization.")

        serializer.save(organization_id=organization)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrganizationInventoryDetailViewSet(RetrieveAPIView):
    serializer_class = OrganizationInventoryDetailSerializer

    def get_object(self):
        org_id = self.kwargs.get("org_id")
        inv_id = self.kwargs.get("inv_id")

        try:
            inventory = OrganizationInventory.objects.get(
                organization__uid=org_id, uid=inv_id
            )
        except OrganizationInventory.DoesNotExist:
            raise NotFound("Organization Inventory not found.")

        return inventory


class OrganizationProductViewSet(ListAPIView):
    serializer_class = OrganizationProductSerializer

    def get_queryset(self):
        org_id = self.kwargs.get("org_id")
        organization = get_object_or_404(Organization, pk=org_id)

        queryset = Product.objects.select_related("organization").filter(
            Q(organization__uid=organization.uid) | Q(organization__uid=None)
        )
        return queryset


class CreateOrganizationInventoryProductViewSet(ListAPIView, CreateAPIView):
    serializer_class = OrganizationInventoryProductSerializer
    permission_classes = [IsAuthenticated, IsOrganizationOwnerOrAdmin]

    def get_queryset(self):
        queryset = OrganizationInventoryProduct.objects.select_related(
            "organization_inventory", "product"
        )

        if not queryset.exists():
            raise NotFound("No product Found")

        return queryset.all()

    def get_serializer_context(self):
        return {"organization": self.kwargs.get("org_id")}

    def perform_create(self, serializer):
        org_id = self.kwargs["org_id"]
        inv_id = self.kwargs["inv_id"]

        organization = get_object_or_404(Organization, uid=org_id)
        inventory = get_object_or_404(
            OrganizationInventory, uid=inv_id, organization=organization
        )

        serializer.save(organization_inventory=inventory)


class OrganizationInventoryProductDetailViewSet(RetrieveUpdateDestroyAPIView):
    serializer_class = OrganizationInventoryProductDetailSerializer
    permission_classes = [IsAuthenticated, IsOrganizationOwnerOrAdmin]

    http_method_names = ["get", "patch", "delete"]

    def get_object(self):
        org_id = self.kwargs.get("org_id")
        inv_id = self.kwargs.get("inv_id")
        product_id = self.kwargs.get("product_id")

        organization = get_object_or_404(Organization, uid=org_id)
        inventory = get_object_or_404(
            OrganizationInventory.objects.select_related("organization"),
            uid=inv_id,
            organization=organization,
        )
        try:
            product = OrganizationInventoryProduct.objects.select_related(
                "product", "organization_inventory"
            ).get(
                organization_inventory=inventory,
                product_id=product_id,
            )
        except OrganizationInventoryProduct.DoesNotExist:
            raise NotFound("Product not found.")

        return product

    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        product_id = self.kwargs["product_id"]

        if not product:
            raise NotFound("Product not found.")

        Product.objects.filter(uid=product_id).delete()
        product.delete()
        return Response(
            {"detail": "Product deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
