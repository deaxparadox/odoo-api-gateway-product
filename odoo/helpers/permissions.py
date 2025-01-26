from rest_framework.permissions import BasePermission

class OnlyVendor(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, "client_vendor")
