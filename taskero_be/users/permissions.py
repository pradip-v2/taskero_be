from rest_framework.permissions import BasePermission


class IsSuperUserOrSelfRequest(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed to the superuser or the user themselves.
        return request.user.is_superuser or obj == request.user

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
