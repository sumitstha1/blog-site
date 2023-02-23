from rest_framework.permissions import BasePermission

class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return  False

class AuthorPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return  False

