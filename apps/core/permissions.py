from rest_framework.permissions import BasePermission


class PublicPostOrAuthenticated(BasePermission):
    """Anonymous may POST once. All other methods require authentication."""

    def has_permission(self, request, view):
        if request.method == "POST":
            return True
        return bool(request.user and request.user.is_authenticated)
