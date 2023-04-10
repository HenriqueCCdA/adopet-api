from rest_framework import serializers

from adopet.pet.models import Pet


class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = (
            "id",
            "name",
            "size",
            "age",
            "behavior",
            "shelter",
            "is_adopted",
            "created_at",
            "modified_at",
        )
