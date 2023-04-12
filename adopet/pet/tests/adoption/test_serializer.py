import pytest
from django.db import DatabaseError
from django.test import RequestFactory

from adopet.pet.models import Adoption
from adopet.pet.serializers import AdoptionSerializer

pytestmark = pytest.mark.django_db


def test_positive_serialization_one_obj(adoption):
    request = RequestFactory().request()

    serializer = AdoptionSerializer(instance=adoption, context={"request": request})

    data = serializer.data

    assert data["id"] == adoption.pk
    assert data["pet"] == adoption.pet.pk
    assert data["tutor"] == adoption.tutor.pk
    assert data["date"] == adoption.date.isoformat()
    assert data["created_at"] == adoption.created_at.astimezone().isoformat()
    assert data["modified_at"] == adoption.modified_at.astimezone().isoformat()


@pytest.mark.parametrize(
    "field",
    [
        "pet",
        "tutor",
        "date",
    ],
)
def test_negative_missing_fields(field, create_adoption_payload):
    data = create_adoption_payload.copy()

    del data[field]

    serializer = AdoptionSerializer(data=data)

    assert not serializer.is_valid()

    assert serializer.errors[field] == ["Este campo é obrigatório."]


@pytest.mark.parametrize(
    "field, value, error",
    [
        ("pet", "a", "Tipo incorreto. Esperado valor pk, recebeu str."),
        ("pet", -1, 'Pk inválido "-1" - objeto não existe.'),
        ("tutor", "a", "Tipo incorreto. Esperado valor pk, recebeu str."),
        ("tutor", -1, 'Pk inválido "-1" - objeto não existe.'),
        ("date", -1, "Formato inválido para data. Use um dos formatos a seguir: YYYY-MM-DD."),
    ],
)
def test_negative_validation_errors(field, value, error, create_adoption_payload):
    data = create_adoption_payload.copy()

    data[field] = value

    serializer = AdoptionSerializer(data=data)

    assert not serializer.is_valid()

    assert serializer.errors[field] == [error]


def test_positive_create(create_adoption_payload):
    serializer = AdoptionSerializer(data=create_adoption_payload)

    assert serializer.is_valid()

    serializer.save()

    adoption = Adoption.objects.first()

    assert adoption.pk
    assert adoption.pet.is_adopted


def test_negativel_create_error_in_change_pet_adopted_info(mocker, create_adoption_payload):
    def raise_():
        raise DatabaseError()

    serializer = AdoptionSerializer(data=create_adoption_payload)

    assert serializer.is_valid()

    mocker.patch("adopet.pet.serializers.AdoptionSerializer._change_to_adopted", new=lambda x, y: raise_())

    with pytest.raises(DatabaseError):
        serializer.save()

    assert not Adoption.objects.exists()
