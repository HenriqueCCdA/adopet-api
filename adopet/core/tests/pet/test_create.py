import pytest
from django.shortcuts import resolve_url
from rest_framework import status

from adopet.core.models import Pet

pytestmark = pytest.mark.django_db


URL = "core:list-create-pet"


def test_positive(client_api_auth_shelter, create_pet_payload):
    url = resolve_url(URL)

    resp = client_api_auth_shelter.post(url, data=create_pet_payload, format="multipart")

    assert resp.status_code == status.HTTP_201_CREATED

    pet = Pet.objects.first()
    body = resp.json()

    assert body["id"] == pet.id
    assert body["name"] == pet.name
    assert body["size"] == pet.size
    assert body["age"] == pet.age
    assert body["behavior"] == pet.behavior
    assert body["shelter"] == pet.shelter.pk
    assert body["photo"] == f"http://testserver{pet.photo.url}"
    assert not body["is_adopted"]
    assert body["created_at"] == str(pet.created_at.astimezone().isoformat())
    assert body["modified_at"] == str(pet.modified_at.astimezone().isoformat())

    assert resp["Location"] == f"http://testserver/pet/{pet.id}/"


def test_negative_must_be_shelter(client_api_auth_user, create_pet_payload):
    url = resolve_url(URL)

    resp = client_api_auth_user.post(url, data=create_pet_payload, format="multipart")

    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    body = resp.json()

    assert body == {"non_field_errors": ["O user precisa ser um abrigo."]}


@pytest.mark.parametrize(
    "field",
    [
        "name",
        "size",
        "age",
        "behavior",
    ],
)
def test_negative_missing_fields(client_api_auth_user, field, create_pet_payload):
    data = create_pet_payload.copy()

    del data[field]

    url = resolve_url(URL)

    resp = client_api_auth_user.post(url, data=data)

    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    assert not Pet.objects.exists()
    body = resp.json()

    assert body[field] == ["Este campo é obrigatório."]


@pytest.mark.parametrize(
    "field, value, error",
    [
        ("name", "a" * 101, "Certifique-se de que este campo não tenha mais de 100 caracteres."),
        ("size", "ab", '"ab" não é um escolha válido.'),
        ("age", -1, "Certifque-se de que este valor seja maior ou igual a 0."),
        ("age", "d-1", "Um número inteiro válido é exigido."),
        ("behavior", "a" * 101, "Certifique-se de que este campo não tenha mais de 100 caracteres."),
    ],
)
def test_negative_validation_errors(client_api_auth_user, field, value, error, create_pet_payload):
    data = create_pet_payload.copy()

    data[field] = value

    url = resolve_url(URL)

    resp = client_api_auth_user.post(url, data=data)

    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    assert not Pet.objects.exists()
    body = resp.json()

    assert body[field] == [error]


def test_negative_must_be_auth(client_api, users):
    url = resolve_url(URL)

    resp = client_api.post(url)

    assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    body = resp.json()

    assert body["detail"] == "As credenciais de autenticação não foram fornecidas."
