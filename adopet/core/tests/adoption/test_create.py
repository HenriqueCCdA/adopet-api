import pytest
from django.shortcuts import resolve_url
from rest_framework import status

from adopet.core.models import Adoption

pytestmark = pytest.mark.django_db


URL = "core:list-create-adoption"


def test_positive(client_api_auth_tutor, create_adoption_payload):
    url = resolve_url(URL)

    resp = client_api_auth_tutor.post(url, data=create_adoption_payload)

    assert resp.status_code == status.HTTP_201_CREATED

    adoption = Adoption.objects.first()
    body = resp.json()

    assert body["id"] == adoption.id
    assert body["pet"] == adoption.pet.pk
    assert body["tutor"] == adoption.tutor.pk
    assert body["date"] == adoption.date.isoformat()
    assert body["created_at"] == adoption.created_at.astimezone().isoformat()
    assert body["modified_at"] == adoption.modified_at.astimezone().isoformat()

    assert adoption.pet.is_adopted

    assert resp["Location"] == f"http://testserver/adoption/{adoption.pk}/"


def test_negative_must_be_tutor(client_api_auth_user, create_adoption_payload):
    url = resolve_url(URL)

    resp = client_api_auth_user.post(url, data=create_adoption_payload)

    assert resp.status_code == status.HTTP_403_FORBIDDEN

    body = resp.json()

    assert body["detail"] == "Você não tem permissão para executar essa ação."


def test_negative_pet_must_be_actived(client_api_auth_tutor, create_adoption_payload, pet):
    data = create_adoption_payload.copy()

    url = resolve_url(URL)

    pet.is_active = False
    pet.save()

    data["pet"] = pet.pk

    resp = client_api_auth_tutor.post(url, data=data)
    assert resp.status_code == status.HTTP_400_BAD_REQUEST


def test_negative_pet_must_not_be_adopted(client_api_auth_tutor, create_adoption_payload, pet):
    data = create_adoption_payload.copy()

    url = resolve_url(URL)

    pet.is_adopted = True
    pet.save()

    data["pet"] = pet.pk

    resp = client_api_auth_tutor.post(url, data=data)
    assert resp.status_code == status.HTTP_400_BAD_REQUEST


def test_negative_tutor_must_be_actived(client_api_auth_tutor, create_adoption_payload, tutor):
    data = create_adoption_payload.copy()

    url = resolve_url(URL)

    tutor.is_active = False
    tutor.save()

    data["tutor"] = tutor.pk

    resp = client_api_auth_tutor.post(url, data=data)
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.parametrize(
    "field",
    [
        "pet",
        "tutor",
        "date",
    ],
)
def test_negative_missing_fields(client_api_auth_tutor, field, create_adoption_payload):
    data = create_adoption_payload.copy()

    del data[field]

    url = resolve_url(URL)

    resp = client_api_auth_tutor.post(url, data=data)

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
def test_negative_validation_errors(client_api_auth_tutor, field, value, error, create_adoption_payload):
    data = create_adoption_payload.copy()

    data[field] = value

    url = resolve_url(URL)

    resp = client_api_auth_tutor.post(url, data=data)

    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    assert not Adoption.objects.exists()
    body = resp.json()

    assert body[field] == [error]


def test_negative_must_be_auth(client_api):
    url = resolve_url(URL)

    resp = client_api.delete(url)

    assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    body = resp.json()

    assert body["detail"] == "As credenciais de autenticação não foram fornecidas."
