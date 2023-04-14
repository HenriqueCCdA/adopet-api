from rest_framework.permissions import BasePermission


class RegisterAuthenticated(BasePermission):
    """
    POST AnonymousUser and User return true
    """

    def has_permission(self, request, view):
        if request.method == "POST":
            return True

        return bool(request.user and request.user.is_authenticated)
