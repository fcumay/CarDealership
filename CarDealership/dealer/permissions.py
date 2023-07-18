from rest_framework import permissions

from customer.models import RoleChoices


class CanCreateDealershipPromotion(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == RoleChoices.is_dealership_admin


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(request.user and request.user.is_staff)
