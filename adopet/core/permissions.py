from rest_framework.permissions import SAFE_METHODS, BasePermission

from adopet.accounts.models import CustomUser as User


class OnlyShelterCanCreateDeleteUpdatePet(BasePermission):
    """Only shelter can delete, update and create a pet"""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.role == User.Role.SHELTER


class ShelterOnlyCanDeleteUpdateOwnPets(OnlyShelterCanCreateDeleteUpdatePet):
    """Shelter only can delete and update own pets"""

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.shelter_id == request.user.pk


class ShelterCanDeleteAdoptionOfYouOwnPets(OnlyShelterCanCreateDeleteUpdatePet):
    """Shelter can delete adoption of you won pets"""

    def has_object_permission(self, request, view, obj):
        return obj.pet.shelter == request.user


class OnlyTutorCanCreateAdoption(BasePermission):
    """ "Only tutor can create a adoption"""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.role == User.Role.TUTOR
