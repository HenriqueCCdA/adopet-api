from rest_framework import serializers

from adopet.pet.models import Adoption, Pet


class PetSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="pet:read-delete-update", read_only=True)

    class Meta:
        model = Pet
        fields = (
            "id",
            "name",
            "size",
            "age",
            "behavior",
            "shelter",
            "url",
            "is_adopted",
            "created_at",
            "modified_at",
        )


class AdoptionSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="pet:read-delete-adoption", read_only=True)

    class Meta:
        model = Adoption
        fields = (
            "id",
            "pet",
            "tutor",
            "date",
            "url",
            "created_at",
            "modified_at",
        )
