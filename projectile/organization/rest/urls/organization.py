from django.urls import path
from organization.rest.views.organization import (
    OrganizationViewSet,
    CreateOrganizationViewSet,
    OrganizationDetailViewSet,
)

urlpatterns = [
    path("", OrganizationViewSet.as_view(), name="organization"),
    path(
        "/<uuid:org_id>",
        OrganizationDetailViewSet.as_view(),
        name="organization-detail",
    ),
    path("/create", CreateOrganizationViewSet.as_view(), name="create-organization"),
]
