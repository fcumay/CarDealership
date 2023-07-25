from rest_framework import permissions

from customer.models import RoleChoices


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user.is_superuser


class CanModifyDealer(permissions.BasePermission):
    def has_permission(self, request, view):
        if (
            request.method in permissions.SAFE_METHODS
            and request.user.role == RoleChoices.is_dealership_admin
        ):
            return True
        else:
            return request.user.is_superuser


class IsAdminOwnerOrReadlOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if (
            request.method == "POST"
            and request.user.role == RoleChoices.is_dealership_admin
        ):
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role in [
            RoleChoices.is_superuser,
            RoleChoices.is_dealership_admin,
        ]

    def has_object_permission(self, request, view, obj):
        if request.user.role == RoleChoices.is_superuser:
            return True
        elif request.user.role == RoleChoices.is_dealership_admin:
            return request.user.email == obj.dealership.owner.email
        return False
