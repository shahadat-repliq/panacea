from rest_framework import permissions

from delivery.models import DeliveryUser


class IsDeliveryUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return DeliveryUser.objects.filter(user=request.user).exists()
