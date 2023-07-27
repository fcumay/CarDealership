from rest_framework import permissions

from customer.models import RoleChoices


class RegistrationPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == "POST"


class Information(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS and view.action == 'list':
            return request.user.is_superuser
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.role == RoleChoices.is_superuser:
            return True
        return request.user.email == obj.email
