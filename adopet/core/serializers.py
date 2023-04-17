from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from adopet.core.models import CustomUser as User


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(label="Senha de confirmação", max_length=128, write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "name",
            "email",
            "is_active",
            "is_tutor",
            "is_shelter",
            "password",
            "password2",
            "url",
            "created_at",
            "modified_at",
        )
        extra_kwargs = {"password": {"write_only": True}}

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
    url = serializers.HyperlinkedIdentityField(view_name="core:read-delete-update-tutor", read_only=True)

    def create(self, validate_data):
        user = super().create(validate_data)
        user.is_tutor = True
        user.save()
        Token.objects.create(user=user)
        return user


class AbrigoSerializer(UserSerializer):  # TODO: nome em portugues
    url = serializers.HyperlinkedIdentityField(view_name="core:read-delete-update-shelter", read_only=True)

    def create(self, validate_data):
        user = super().create(validate_data)
        user.is_shelter = True
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


class VersionSerializer(serializers.Serializer):
    version = serializers.FloatField()
