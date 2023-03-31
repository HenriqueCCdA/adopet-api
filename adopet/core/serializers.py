from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from adopet.core.models import CustomUser as User


class TutorSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(label="Senha de confimação", max_length=128, write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "name",
            "email",
            "is_active",
            "password",
            "password2",
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
