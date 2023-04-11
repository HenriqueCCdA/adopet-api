import pytest
from django.shortcuts import resolve_url
from rest_framework import status

from adopet.pet.models import Adoption

pytestmark = pytest.mark.django_db


URL = "pet:create-adoption"


def test_positive(client_api, create_adoption_payload):
    url = resolve_url(URL)

    resp = client_api.post(url, data=create_adoption_payload)
    assert resp.status_code == status.HTTP_201_CREATED

    adoption = Adoption.objects.first()
    body = resp.json()

    assert body["id"] == adoption.id
    assert body["pet"] == adoption.pet.pk
    assert body["tutor"] == adoption.tutor.pk
    assert body["date"] == adoption.date.isoformat()
    assert body["created_at"] == adoption.created_at.astimezone().isoformat()
    assert body["modified_at"] == adoption.modified_at.astimezone().isoformat()

    assert resp["Location"] == f"http://testserver/adoption/{adoption.pk}/"


@pytest.mark.parametrize(
    "field",
    [
        "pet",
        "tutor",
        "date",
    ],
)
def test_negative_missing_fields(client_api, field, create_adoption_payload):
    data = create_adoption_payload.copy()

    del data[field]

    url = resolve_url(URL)

    resp = client_api.post(url, data=data)

    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    assert not Adoption.objects.exists()
    body = resp.json()

    assert body[field] == ["Este campo é obrigatório."]


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
def test_negative_validation_errors(client_api, field, value, error, create_adoption_payload):
    data = create_adoption_payload.copy()

    data[field] = value

    url = resolve_url(URL)

    resp = client_api.post(url, data=data)

    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    assert not Adoption.objects.exists()
    body = resp.json()

    assert body[field] == [error]
