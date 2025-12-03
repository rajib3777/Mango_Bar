from rest_framework.permissions import BasePermission


class IsAdminSeller(BasePermission):
    def has_permission(self, request, view):
        if request.method in ("POST", "PUT", "PATCH", "DELETE"):   
            return True
        
        
        return (
            request.user.is_authenticated and 
            (request.user.is_superuser or getattr(request.user, "role", "") == "Seller")
        )