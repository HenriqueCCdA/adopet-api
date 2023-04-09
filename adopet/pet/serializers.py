from rest_framework import serializers

from adopet.pet.models import Pet


class PetSerializer(serializers.ModelSerializer):
    size = serializers.SerializerMethodField()

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

    def get_size(self, obj):
        return obj.get_size_display()
