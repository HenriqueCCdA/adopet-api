import pytest
from django.test import RequestFactory
from rest_framework.authtoken.models import Token

from adopet.core.models import CustomUser as User
from adopet.core.serializers import ShelterSerializer

pytestmark = pytest.mark.django_db


def test_positive_create(create_tutor_payload):
    serializer = ShelterSerializer(data=create_tutor_payload)

    assert serializer.is_valid()

    shelter = serializer.save()
    assert User.objects.exists()
    assert Token.objects.get(user=shelter)
    assert shelter.role == User.Role.SHELTER


def test_positive_serialization_objs_list(users):
    request = RequestFactory().request()

    serializer = ShelterSerializer(instance=User.objects.all(), many=True, context={"request": request})

    for data, db in zip(serializer.data, users):
        assert data["id"] == db.id
        assert data["name"] == db.name
        assert data["email"] == db.email
        assert "password" not in data
        assert "password2" not in data
        assert data["is_active"] == db.is_active
        assert data["created_at"] == str(db.created_at.astimezone().isoformat())
        assert data["modified_at"] == str(db.modified_at.astimezone().isoformat())


def test_positive_serialization_one_obj(users):
    shelter = users[2]

    request = RequestFactory().request()

    serializer = ShelterSerializer(instance=shelter, context={"request": request})

    data = serializer.data

    assert data["id"] == shelter.id
    assert data["name"] == shelter.name
    assert data["email"] == shelter.email
    assert "password" not in data
    assert "password2" not in data
    assert data["is_active"] == shelter.is_active
    assert data["created_at"] == str(shelter.created_at.astimezone().isoformat())
    assert data["modified_at"] == str(shelter.modified_at.astimezone().isoformat())
    assert data["url"] == f"http://testserver/abrigos/{shelter.id}/"
