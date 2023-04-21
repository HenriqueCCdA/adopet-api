from django.db import transaction
from rest_framework import serializers

from adopet.core.models import Adoption, Pet


class PetSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="core:read-delete-update-pet", read_only=True)

    class Meta:
        model = Pet
        fields = (
            "id",
            "name",
            "size",
            "age",
            "behavior",
            "shelter",
            "photo",
            "url",
            "is_adopted",
            "created_at",
            "modified_at",
        )


class AdoptionSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="core:read-delete-adoption", read_only=True)

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

    def create(self, validate_data):
        with transaction.atomic():
            adoption = super().create(validate_data)
            self._change_to_adopted(adoption.pet)
            return adoption

    def _change_to_adopted(self, pet):
        pet.is_adopted = True
        pet.save()
