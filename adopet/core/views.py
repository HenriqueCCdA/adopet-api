from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from adopet.core.permissions import DeleteUpdateUserObjPermission, RegisterPermission
from adopet.core.paginators import MyPagination
from adopet.core.serializers import AbrigoSerializer, TutorSerializer

User = get_user_model()


class Whoami(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        role = None

        if user.is_tutor:
            role = "tutor"
        elif user.is_shelter:
            role = "shelter"

        data = {"id": user.pk, "name": user.name, "email": user.email, "role": role}

        return Response(data)


class Version(APIView):
    def get(self, request):
        return Response({"version": 3.0})


class TutorLC(ListCreateAPIView):
    """
    View for Create or List a Tutor

    POST: Register new tutor. Not need to be auth
    GET: List tutors. Need to be auth
    """

    queryset = User.objects.tutor()
    serializer_class = TutorSerializer
    pagination_class = MyPagination
    permission_classes = [RegisterPermission]


class TutorRDU(RetrieveUpdateDestroyAPIView):
    """
    View for Read, Delete and Update a Tutor

    Need to be auth
    """

    queryset = User.objects.tutor()
    serializer_class = TutorSerializer
    permission_classes = [IsAuthenticated, DeleteUpdateUserObjPermission]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(data={"msg": "Tutor deletado com sucesso."}, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        """Soft delete"""
        instance.is_active = False
        instance.save()

    def put(self, request, *args, **kwargs):
        return Response({"detail": 'Method "PUT" not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ShelterLC(ListCreateAPIView):
    """
    View for Create or List a shelter

    POST: Register new shelter. Not need to be auth
    GET: List shelters. Need to be auth
    """

    queryset = User.objects.shelter()
    serializer_class = AbrigoSerializer
    pagination_class = MyPagination
    permission_classes = [RegisterPermission]


class ShelterRDU(RetrieveUpdateDestroyAPIView):
    """
    View for Read, Delete and Update a shelter

    Need to be auth
    """

    queryset = User.objects.shelter()
    serializer_class = AbrigoSerializer
    permission_classes = [IsAuthenticated, DeleteUpdateUserObjPermission]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(data={"msg": "Abrigo deletado com sucesso."}, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        """Soft delete"""
        instance.is_active = False
        instance.save()

    def put(self, request, *args, **kwargs):
        return Response({"detail": 'Method "PUT" not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


tutor_list_create = TutorLC.as_view()
tutor_read_delete_update = TutorRDU.as_view()

shelter_list_create = ShelterLC.as_view()
shelter_read_delete_update = ShelterRDU.as_view()

version = Version.as_view()
whoami = Whoami.as_view()
