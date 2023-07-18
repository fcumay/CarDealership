from rest_framework import permissions

from customer.models import RoleChoices


class CanModifyDealership(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role in [
            RoleChoices.is_superuser,
            RoleChoices.is_dealership_admin,
        ]
    def has_object_permission(self, request, view, obj):
        if request.user.role == RoleChoices.is_superuser:
            return True
        elif request.user.role == RoleChoices.is_dealership_admin:
            if request.method == 'PUT':
                if 'balance' in request.data or 'owner' in request.data:
                    return False
            return request.user.email == obj.owner.email
        return False


