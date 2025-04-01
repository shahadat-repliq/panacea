from rest_framework import permissions

from organization.models import OrganizationUser


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
