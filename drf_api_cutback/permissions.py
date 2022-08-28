from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to handle app functionality for owners.
    """

    def has_object_permission(self, request, view, obj):
        """
        The request is authenticated as an owner, or is a read-only request.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user and
            request.user.is_authenticated and
            request.user.email_verified
        )
