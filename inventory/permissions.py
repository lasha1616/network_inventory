# inventory/permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    Admin: full CRUD on everything.
    Regular user: read only.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_staff or request.user.is_superuser


class IsAdminOrOwner(BasePermission):
    """
    Admin: full CRUD on everything.
    Regular user: can create, and can edit/delete only their own items.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        # Allow all authenticated users to read and create
        if request.method in SAFE_METHODS or request.method == 'POST':
            return True
        return True  # object-level check handles the rest

    def has_object_permission(self, request, view, obj):
        # Read is allowed for everyone
        if request.method in SAFE_METHODS:
            return True
        # Admin can do anything
        if request.user.is_staff or request.user.is_superuser:
            return True
        # Owner can edit/delete their own
        return obj.created_by == request.user