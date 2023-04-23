import pytest
from django.shortcuts import resolve_url
from rest_framework import status

from adopet.core.models import Pet

pytestmark = pytest.mark.django_db


URL = "core:read-delete-update-pet"


def test_positive(client_api_auth_shelter, pet):
    pk = pet.pk

    data = {"name": "Update name"}

    url = resolve_url(URL, pk=pk)

    resp = client_api_auth_shelter.patch(url, data=data)

    assert resp.status_code == status.HTTP_200_OK
    body = resp.json()

    assert body["name"] == "Update name"


def test_negative_only_shelter_can_update_pet(client_api_auth_user, pet):
    pk = pet.pk

    url = resolve_url(URL, pk=pk)

    resp = client_api_auth_user.delete(url)

    assert resp.status_code == status.HTTP_403_FORBIDDEN

    body = resp.json()

    assert body["detail"] == "Você não tem permissão para executar essa ação."


def test_negative_invalid_id(client_api_auth_shelter, pets):
    url = resolve_url(URL, pk=444444)

    resp = client_api_auth_shelter.patch(url)

    assert resp.status_code == status.HTTP_404_NOT_FOUND

    body = resp.json()

    assert body["detail"] == "Não encontrado."


def test_negative_tutor_inactive_must_return_404(client_api_auth_shelter, pets):
    pk = Pet.objects.filter(is_active=False).values_list("pk").first()[0]

    url = resolve_url(URL, pk=pk)

    resp = client_api_auth_shelter.patch(url)

    assert resp.status_code == status.HTTP_404_NOT_FOUND

    body = resp.json()

    assert body["detail"] == "Não encontrado."


@pytest.mark.parametrize(
    "field, value, err",
    [
        ("age", -2, "Certifque-se de que este valor seja maior ou igual a 0."),
        ("age", "not number", "Um número inteiro válido é exigido."),
        ("size", "DB", '"DB" não é um escolha válido.'),
    ],
)
def test_negative_invalid_field(client_api_auth_shelter, field, value, err, pet):
    pk = pet.pk

    data = {field: value}

    url = resolve_url(URL, pk=pk)

    resp = client_api_auth_shelter.patch(url, data=data)

    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    body = resp.json()

    assert body[field] == [err]


def test_negative_put_is_not_allowed(client_api_auth_shelter, pets):
    pk = Pet.objects.filter(is_active=False).values_list("pk").first()[0]

    url = resolve_url(URL, pk=pk)

    resp = client_api_auth_shelter.put(url)

    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    body = resp.json()

    assert body["detail"] == 'Method "PUT" not allowed.'


def test_negative_must_be_auth(client_api, users):
    url = resolve_url(URL, pk=1)

    resp = client_api.get(url)

    assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    body = resp.json()

    assert body["detail"] == "As credenciais de autenticação não foram fornecidas."
