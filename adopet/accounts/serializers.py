from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from adopet.accounts.models import CustomUser as User


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(label="Senha de confirmação", max_length=128, write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "name",
            "email",
            "city",
            "phone",
            "about",
            "is_active",
            "role",
            "password",
            "password2",
            "url",
            "created_at",
            "modified_at",
        )
        extra_kwargs = {
            "password": {"write_only": True},
            "is_active": {"read_only": True},
            "role": {"read_only": True},
        }

    def create(self, validate_data):
        user = User.objects.create_user(
            name=validate_data["name"],
            email=validate_data["email"],
            password=validate_data["password"],
        )
        return user

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")
        if password != password2:
            raise serializers.ValidationError("Password não são iguais.")

        return attrs

    def validate_password(self, value):
        validate_password(value)
        return value


class TutorSerializer(UserSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="accounts:read-delete-update-tutor", read_only=True)

    def create(self, validate_data):
        with transaction.atomic():
            user = super().create(validate_data)
            user.role = User.Role.TUTOR
            user.save()
            Token.objects.create(user=user)
        return user


class ShelterSerializer(UserSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="accounts:read-delete-update-shelter", read_only=True)

    def create(self, validate_data):
        with transaction.atomic():
            user = super().create(validate_data)
            user.role = User.Role.SHELTER
            user.save()
            Token.objects.create(user=user)
        return user

    # TODO: adiciona a campo pets


class WhoamiSerializer(serializers.ModelSerializer):
    role = serializers.CharField(max_length=10)

    class Meta:
        model = User
        fields = (
            "id",
            "name",
            "email",
            "role",
        )
        extra_kwargs = {
            "name": {"read_only": True},
            "email": {"read_only": True},
            "role": {"read_only": True},
        }


class VersionSerializer(serializers.Serializer):
    version = serializers.FloatField(read_only=True)
