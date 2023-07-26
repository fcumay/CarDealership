from rest_framework import permissions

from customer.models import RoleChoices


class RegistrationPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == "POST"


class Information(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in ["POST", "UPDATE"]

    def has_object_permission(self, request, view, obj):
        if request.user.role == RoleChoices.is_superuser:
            return True
        return request.user.email == obj.email
