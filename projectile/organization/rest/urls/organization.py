from django.urls import path
from organization.rest.views.organization import (
    OrganizationViewSet,
    CreateOrganizationViewSet,
    OrganizationDetailViewSet,
    OrganizationInventoryViewSet,
    CreateOrganizationInventoryViewSet,
    OrganizationProductViewSet,
    OrganizationInventoryDetailViewSet,
    CreateOrganizationInventoryProductViewSet,
    OrganizationInventoryProductDetailViewSet,
)

urlpatterns = [
    path("", OrganizationViewSet.as_view(), name="organization"),
    path(
        "/<uuid:org_id>",
        OrganizationDetailViewSet.as_view(),
        name="organization-detail",
    ),
    path(
        "/<uuid:org_id>/inventory",
        OrganizationInventoryViewSet.as_view(),
        name="organization-inventory",
    ),
    path(
        "/<uuid:org_id>/inventory/create",
        CreateOrganizationInventoryViewSet.as_view(),
        name="create-organization-inventory",
    ),
    path(
        "/<uuid:org_id>/inventory/<uuid:inv_id>",
        OrganizationInventoryDetailViewSet.as_view(),
        name="organization-inventory-detail",
    ),
    path(
        "/<uuid:org_id>/product",
        OrganizationProductViewSet.as_view(),
        name="organization-product",
    ),
    path(
        "/<uuid:org_id>/inventory/<uuid:inv_id>/product",
        CreateOrganizationInventoryProductViewSet.as_view(),
        name="create-organization-product",
    ),
    path(
        "/<uuid:org_id>/inventory/<uuid:inv_id>/product/<uuid:product_id>",
        OrganizationInventoryProductDetailViewSet.as_view(),
        name="organization-inventory-product-detail",
    ),
    path("/create", CreateOrganizationViewSet.as_view(), name="create-organization"),
]
