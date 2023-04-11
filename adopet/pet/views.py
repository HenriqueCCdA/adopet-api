from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    ListCreateAPIView,
    RetrieveDestroyAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.response import Response

from adopet.core.paginators import MyPagination
from adopet.pet.models import Adoption, Pet
from adopet.pet.serializers import AdoptionSerializer, PetSerializer


class PetLC(ListCreateAPIView):
    queryset = Pet.objects.filter(is_active=True)  # TODO cria o maneger para isso-
    serializer_class = PetSerializer
    pagination_class = MyPagination


class PetRDU(RetrieveUpdateDestroyAPIView):
    queryset = Pet.objects.filter(is_active=True)  # TODO cria o maneger para isso
    serializer_class = PetSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(data={"msg": "Abrigo deletado com sucesso."}, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    def put(self, request, *args, **kwargs):
        return Response({"detail": 'Method "PUT" not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class AdoptionC(CreateAPIView):
    queryset = Adoption.objects.filter(is_active=True)  # TODO cria o maneger para isso
    serializer_class = AdoptionSerializer


class AdoptionRD(RetrieveDestroyAPIView):
    queryset = Adoption.objects.filter(is_active=True)  # TODO cria o maneger para isso
    serializer_class = AdoptionSerializer


rdu_pet = PetRDU.as_view()
lc_pet = PetLC.as_view()
c_adoption = AdoptionC.as_view()
rd_adoption = AdoptionRD.as_view()
