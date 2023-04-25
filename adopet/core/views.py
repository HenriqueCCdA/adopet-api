from django.db import transaction
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveDestroyAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from adopet.accounts.models import CustomUser as User
from adopet.accounts.paginators import MyPagination
from adopet.core.models import Adoption, Pet
from adopet.core.permissions import (
    OnlyShelterCanCreateDeleteUpdatePet,
    OnlyTutorCanCreateAdoption,
    ShelterCanDeleteAdoptionOfYouOwnPets,
    ShelterOnlyCanDeleteUpdateOwnPets,
)
from adopet.core.serializers import AdoptionSerializer, PetSerializer


class PetLC(ListCreateAPIView):
    queryset = Pet.objects.filter(is_active=True)  # TODO cria o maneger para isso-
    serializer_class = PetSerializer
    pagination_class = MyPagination
    permission_classes = [IsAuthenticated, OnlyShelterCanCreateDeleteUpdatePet]
    parser_classes = [MultiPartParser]


class PetRDU(RetrieveUpdateDestroyAPIView):
    queryset = Pet.objects.filter(is_active=True)  # TODO cria o maneger para isso
    serializer_class = PetSerializer
    permission_classes = [
        IsAuthenticated,
        ShelterOnlyCanDeleteUpdateOwnPets,
    ]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(data={"detail": "Pet deletado com sucesso."}, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        """Soft delete"""
        instance.is_active = False
        instance.save()

    @extend_schema(methods=["PUT"], exclude=True)
    def put(self, request, *args, **kwargs):
        return Response({"detail": 'Method "PUT" not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class AdoptionLC(ListCreateAPIView):
    queryset = Adoption.objects.all()
    serializer_class = AdoptionSerializer
    permission_classes = [
        IsAuthenticated,
        OnlyTutorCanCreateAdoption,
    ]

    def get_queryset(self):
        user = self.request.user

        qs = super().get_queryset()

        if user.role == User.Role.TUTOR:
            qs = qs.filter(tutor=user)
        elif user.role == User.Role.SHELTER:
            qs = qs.filter(pet__shelter=user)

        return qs


class AdoptionRD(RetrieveDestroyAPIView):
    """Only shelter can delete a adoption"""

    queryset = Adoption.objects.all()
    serializer_class = AdoptionSerializer
    permission_classes = [
        IsAuthenticated,
        ShelterCanDeleteAdoptionOfYouOwnPets,
    ]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(data={"detail": "Adoção deletada com sucesso."}, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        """Hard delete and set pet.is_adopted to False"""
        instance.pet.is_adopted = False
        with transaction.atomic():
            instance.pet.save()
            instance.delete()


rdu_pet = PetRDU.as_view()
lc_pet = PetLC.as_view()
lc_adoption = AdoptionLC.as_view()
rd_adoption = AdoptionRD.as_view()
