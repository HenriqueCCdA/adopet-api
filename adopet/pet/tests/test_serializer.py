import pytest

from adopet.pet.models import Pet
from adopet.pet.serializers import PetSerializer

pytestmark = pytest.mark.django_db


def test_positive_serialization_objs_list(pets):
    serializer = PetSerializer(instance=Pet.objects.all(), many=True)

    for data, db in zip(serializer.data, pets):
        assert data["id"] == db.id
        assert data["name"] == db.name
        assert data["size"] == db.size
        assert data["age"] == db.age
        assert data["behavior"] == db.behavior
        assert data["shelter"] == db.shelter.pk
        assert data["is_adopted"] == db.is_adopted
        assert data["created_at"] == str(db.created_at.astimezone().isoformat())
        assert data["modified_at"] == str(db.modified_at.astimezone().isoformat())


def test_positive_serialization_one_obj(pet):
    serializer = PetSerializer(instance=pet)

    data = serializer.data

    assert data["id"] == pet.pk
    assert data["name"] == pet.name
    assert data["size"] == pet.size
    assert data["age"] == pet.age
    assert data["behavior"] == pet.behavior
    assert data["shelter"] == pet.shelter.pk
    assert data["is_adopted"] == pet.is_adopted
    assert data["created_at"] == str(pet.created_at.astimezone().isoformat())
    assert data["modified_at"] == str(pet.modified_at.astimezone().isoformat())


def test_positive_metadata_fields():
    serializer = PetSerializer()

    assert serializer.fields["name"].max_length == 100

    assert serializer.fields["age"].max_value == 32767
    assert serializer.fields["age"].min_value == 0

    assert serializer.fields["behavior"].max_length == 100


# TODO Testa depois a parte da validação e criação
