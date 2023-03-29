from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveDestroyAPIView
from rest_framework.response import Response

from adopet.core.paginators import MyPagination
from adopet.core.serializers import TutorListSerializer

User = get_user_model()


class TutorList(ListAPIView):
    queryset = User.objects.filter(is_tutor=True, is_active=True)
    serializer_class = TutorListSerializer
    pagination_class = MyPagination


class TutorDetailDelete(RetrieveDestroyAPIView):
    queryset = User.objects.filter(is_tutor=True, is_active=True)
    serializer_class = TutorListSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(data={"msg": "Tutor deletado com sucesso."}, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
