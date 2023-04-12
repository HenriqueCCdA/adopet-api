import pytest
from django.test import RequestFactory

from adopet.pet.models import Pet
from adopet.pet.serializers import PetSerializer

pytestmark = pytest.mark.django_db


def test_positive_serialization_objs_list(pets):
    request = RequestFactory().request()

    serializer = PetSerializer(instance=Pet.objects.all(), many=True, context={"request": request})

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
    request = RequestFactory().request()

    serializer = PetSerializer(instance=pet, context={"request": request})

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


@pytest.mark.parametrize(
    "field",
    [
        "name",
        "size",
        "age",
        "behavior",
        "shelter",
    ],
)
def test_negative_missing_fields(field, create_pet_payload):
    data = create_pet_payload.copy()

    del data[field]

    serializer = PetSerializer(data=data)

    assert not serializer.is_valid()

    assert serializer.errors[field] == ["Este campo é obrigatório."]


@pytest.mark.parametrize(
    "field, value, error",
    [
        ("name", "a" * 101, "Certifique-se de que este campo não tenha mais de 100 caracteres."),
        ("size", "ab", '"ab" não é um escolha válido.'),
        ("age", -1, "Certifque-se de que este valor seja maior ou igual a 0."),
        ("age", "d-1", "Um número inteiro válido é exigido."),
        ("behavior", "a" * 101, "Certifique-se de que este campo não tenha mais de 100 caracteres."),
        ("shelter", 11111, 'Pk inválido "11111" - objeto não existe.'),
        ("shelter", "dd", "Tipo incorreto. Esperado valor pk, recebeu str."),
    ],
)
def test_negative_validation_errors(field, value, error, create_pet_payload):
    data = create_pet_payload.copy()

    data[field] = value

    serializer = PetSerializer(data=data)

    assert not serializer.is_valid()

    assert serializer.errors[field] == [error]


def test_positive_create(create_pet_payload):
    serializer = PetSerializer(data=create_pet_payload)

    assert serializer.is_valid()

    serializer.save()

    assert Pet.objects.exists()
