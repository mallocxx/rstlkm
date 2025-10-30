from rest_framework.permissions import BasePermission, SAFE_METHODS

class RolePermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        role = getattr(getattr(user, 'profile', None), 'role', 'engineer')
        # Admin always allowed
        if role == 'admin' or user.is_superuser:
            return True
        # Supervisor: allow GET on all, write limited (views can override)
        if role == 'supervisor':
            return request.method in SAFE_METHODS
        # Engineer: allow read, and write to visits/surveys/buildings/apartments
        return True
