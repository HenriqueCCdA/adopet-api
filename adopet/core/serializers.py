from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from adopet.accounts.models import CustomUser as User
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

        extra_kwargs = {
            "is_adopted": {"read_only": True},
            "shelter": {"read_only": True},
        }

    def create(self, validate_data):
        """Shelter id is get from request"""

        data = {**validate_data, "shelter": self.context["request"].user}

        pet = super().create(data)

        return pet

    def validate(self, attrs):
        try:
            user = self.context["request"].user
        except (KeyError, AttributeError):
            raise ValidationError("O user precisa estar no contexto.", code="invalid")

        if user.role != User.Role.SHELTER:
            raise ValidationError("O user precisa ser um abrigo.", code="invalid")

        return super().validate(attrs)


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
