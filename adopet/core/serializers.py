from rest_framework import serializers

from adopet.core.models import CustomUser


class TutorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "name", "email", "is_active", "created_at", "modified_at")
