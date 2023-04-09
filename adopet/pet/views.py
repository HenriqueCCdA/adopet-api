from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from adopet.core.paginators import MyPagination
from adopet.pet.models import Pet
from adopet.pet.serializers import PetSerializer


class PetLC(ListCreateAPIView):
    queryset = Pet.objects.filter(is_active=True)
    serializer_class = PetSerializer
    pagination_class = MyPagination


class PetRDU(RetrieveUpdateDestroyAPIView):
    queryset = Pet.objects.filter(is_active=True)
    serializer_class = PetSerializer


rdu_pet = PetRDU.as_view()
lc_pet = PetLC.as_view()
