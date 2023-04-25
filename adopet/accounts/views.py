from django.contrib.auth import get_user_model
from django.db import transaction
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from adopet.accounts.paginators import MyPagination
from adopet.accounts.permissions import (
    DeleteUpdateOnlyMyOwnObj,
    IsAuthenticatedOrRegister,
)
from adopet.accounts.serializers import (
    ShelterSerializer,
    TutorSerializer,
    VersionSerializer,
    WhoamiSerializer,
)

User = get_user_model()


class Whoami(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=WhoamiSerializer)
    def get(self, request):
        """Retorna o usuário que pertence o Token"""
        user = request.user

        data = {"id": user.pk, "name": user.name, "email": user.email, "role": user.get_role_display()}

        serialize = WhoamiSerializer(instance=data)

        return Response(serialize.data)


class Version(APIView):
    permission_classes = [AllowAny]

    @extend_schema(responses=VersionSerializer)
    def get(self, request):
        """Versão da api"""

        serialize = VersionSerializer(instance={"version": 1.0})

        return Response(serialize.data)


class TutorLC(ListCreateAPIView):
    """
    - **POST**: Register new tutor not need to be auth
    - **GET**: List tutors need to be auth
    """

    queryset = User.objects.tutor()
    serializer_class = TutorSerializer
    pagination_class = MyPagination
    permission_classes = [IsAuthenticatedOrRegister]


class TutorRDU(RetrieveUpdateDestroyAPIView):
    """**Read**, **Delete** and **Update** a Tutor need to be auth."""

    DELETE_detail = {"detail": "Tutor deletado com sucesso."}

    queryset = User.objects.tutor()
    serializer_class = TutorSerializer
    permission_classes = [IsAuthenticated, DeleteUpdateOnlyMyOwnObj]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(data={"detail": "Tutor deletado com sucesso."}, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        """Soft delete"""
        instance.is_active = False
        instance.save()

    @extend_schema(methods=["PUT"], exclude=True)
    def put(self, request, *args, **kwargs):
        return Response({"detail": 'Method "PUT" not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ShelterLC(ListCreateAPIView):
    """
    - **POST**: Register new shelter not need to be auth
    - **GET**: List shelters need to be auth
    """

    queryset = User.objects.shelter()
    serializer_class = ShelterSerializer
    pagination_class = MyPagination
    permission_classes = [IsAuthenticatedOrRegister]


class ShelterRDU(RetrieveUpdateDestroyAPIView):
    """**Read**, **Delete** and **Update** a shelter need to be auth."""

    queryset = User.objects.shelter()
    serializer_class = ShelterSerializer
    permission_classes = [IsAuthenticated, DeleteUpdateOnlyMyOwnObj]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(data={"detail": "Abrigo deletado com sucesso."}, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        """Soft delete"""
        with transaction.atomic():
            instance.is_active = False
            instance.pets.update(is_active=False)
            instance.save()

    @extend_schema(methods=["PUT"], exclude=True)
    def put(self, request, *args, **kwargs):
        return Response({"detail": 'Method "PUT" not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


tutor_list_create = TutorLC.as_view()
tutor_read_delete_update = TutorRDU.as_view()

shelter_list_create = ShelterLC.as_view()
shelter_read_delete_update = ShelterRDU.as_view()

version = Version.as_view()
whoami = Whoami.as_view()
