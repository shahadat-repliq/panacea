from rest_framework import viewsets
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status

from organization.models import Organization
from organization.rest.serializers.organization import (
    OrganizationSerializer,
    CreateOrganizationSerializer,
    OrganizationDetailSerializer,
)

from rest_framework.exceptions import NotFound


class OrganizationViewSet(ListAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


class OrganizationDetailViewSet(RetrieveAPIView):
    serializer_class = OrganizationDetailSerializer

    def get_object(self):
        org_id = self.kwargs.get("org_id")

        try:
            organization = Organization.objects.get(uid=org_id)
        except Organization.DoesNotExist:
            raise NotFound("Organization not found.")
        return organization


class CreateOrganizationViewSet(CreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = CreateOrganizationSerializer
