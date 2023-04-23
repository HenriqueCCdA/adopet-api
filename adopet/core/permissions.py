from rest_framework.permissions import SAFE_METHODS, BasePermission

from adopet.accounts.models import CustomUser as User


class ShelterOnlyCanDeleteUpdateOwnPets(BasePermission):
    """Shelter only can delete and update own pets"""

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if obj.shelter_id == request.user.pk:
            return True

        return False


class OnlyShelterCanCreateDeleteUpdatePet(BasePermission):
    """Only shelter can delete, update and create a pet"""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        if request.user.role == User.Role.SHELTER:
            return True

        return False
