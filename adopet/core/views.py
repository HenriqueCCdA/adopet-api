from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from adopet.core.paginators import MyPagination
from adopet.core.serializers import AbrigoSerializer, TutorSerializer

User = get_user_model()


class TutorLC(ListCreateAPIView):
    queryset = User.objects.filter(is_tutor=True, is_shelter=False, is_active=True)
    serializer_class = TutorSerializer
    pagination_class = MyPagination


class TutorRDU(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.filter(is_tutor=True, is_shelter=False, is_active=True)
    serializer_class = TutorSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(data={"msg": "Tutor deletado com sucesso."}, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    def put(self, request, *args, **kwargs):
        return Response({"detail": 'Method "PUT" not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ShelterLC(ListCreateAPIView):
    queryset = User.objects.filter(is_tutor=False, is_shelter=True, is_active=True)
    serializer_class = AbrigoSerializer
    pagination_class = MyPagination


class ShelterRDU(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.filter(is_tutor=False, is_shelter=True, is_active=True)
    serializer_class = AbrigoSerializer


shelter_list_create = ShelterLC.as_view()
shelter_read_delete_update = ShelterRDU.as_view()
