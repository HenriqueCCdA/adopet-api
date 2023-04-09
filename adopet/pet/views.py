from rest_framework.generics import RetrieveUpdateDestroyAPIView

from adopet.pet.models import Pet
from adopet.pet.serializers import PetSerializer


class PetRDU(RetrieveUpdateDestroyAPIView):
    queryset = Pet.objects.filter(is_active=True)
    serializer_class = PetSerializer


rdu_pet = PetRDU.as_view()
