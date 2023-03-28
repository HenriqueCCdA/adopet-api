from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView

from adopet.core.paginators import MyPagination
from adopet.core.serializers import TutorListSerializer

User = get_user_model()


class TutorList(ListAPIView):
    queryset = User.objects.filter(is_tutor=True, is_active=True)
    serializer_class = TutorListSerializer
    pagination_class = MyPagination
