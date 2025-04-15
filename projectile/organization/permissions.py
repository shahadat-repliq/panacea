from rest_framework import permissions

from organization.models import OrganizationUser
from shared.choices import UserRole


class IsOrganizationOwnerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        org_id = view.kwargs.get("org_id")
        user = request.user.uid

        try:
            org_user = OrganizationUser.objects.select_related(
                "user",
                "organization",
            ).get(organization_id=org_id, user__uid=user)
            return org_user.role in ["ADMIN", "OWNER"]
        except OrganizationUser.DoesNotExist:
            return False


class IsBaseOrganizationOwnerOrAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        return (
            OrganizationUser.objects.select_related("user", "organization")
            .filter(user=user, role__in=[UserRole.OWNER, UserRole.ADMIN])
            .exists()
        )
