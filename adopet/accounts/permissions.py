from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthenticatedOrRegister(BasePermission):
    """
    POST AnonymousUser and User return true
    LIST only User return true
    """

    def has_permission(self, request, view):
        if request.method == "POST":
            return True

        return bool(request.user and request.user.is_authenticated)


class DeleteUpdateOnlyMyOwnObj(BasePermission):
    """Only user can update or delete itself"""

    methods = ["DELETE", "PUT", "PATCH"]

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if request.method in self.methods:
            return obj.pk == request.user.pk

        return False
