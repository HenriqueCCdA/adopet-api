import pytest
from django.test import RequestFactory
from rest_framework.authtoken.models import Token

from adopet.accounts.models import CustomUser as User
from adopet.accounts.serializers import TutorSerializer

pytestmark = pytest.mark.django_db


def test_positive_create(create_tutor_payload):
    serializer = TutorSerializer(data=create_tutor_payload)

    assert serializer.is_valid()

    tutor = serializer.save()
    assert User.objects.exists()
    assert Token.objects.get(user=tutor)
    assert tutor.role == User.Role.TUTOR


def test_positive_serialization_objs_list(users):
    request = RequestFactory().request()

    serializer = TutorSerializer(instance=User.objects.all(), many=True, context={"request": request})

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
    tutor = users[2]

    request = RequestFactory().request()

    serializer = TutorSerializer(instance=tutor, context={"request": request})

    data = serializer.data

    assert data["id"] == tutor.id
    assert data["name"] == tutor.name
    assert data["email"] == tutor.email
    assert "password" not in data
    assert "password2" not in data
    assert data["is_active"] == tutor.is_active
    assert data["created_at"] == str(tutor.created_at.astimezone().isoformat())
    assert data["modified_at"] == str(tutor.modified_at.astimezone().isoformat())
    assert data["url"] == f"http://testserver/tutores/{tutor.id}/"
