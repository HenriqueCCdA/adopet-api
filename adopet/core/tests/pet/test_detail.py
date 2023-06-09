import pytest
from django.shortcuts import resolve_url
from rest_framework import status

from adopet.core.models import Pet

pytestmark = pytest.mark.django_db


URL = "core:read-delete-update-pet"


def test_positive_get_by_id(client_api_auth_user, pet):
    pk = pet.pk

    url = resolve_url(URL, pk=pk)

    resp = client_api_auth_user.get(url)

    assert resp.status_code == status.HTTP_200_OK

    body = resp.json()

    assert body["id"] == pet.id
    assert body["name"] == pet.name
    assert body["size"] == pet.size
    assert body["age"] == pet.age
    assert body["behavior"] == pet.behavior
    assert body["shelter"] == pet.shelter.pk
    assert body["photo"] == "http://testserver" + pet.photo.url
    assert not body["is_adopted"]
    assert body["created_at"] == str(pet.created_at.astimezone().isoformat())
    assert body["modified_at"] == str(pet.modified_at.astimezone().isoformat())


def test_negative_invalid_id(client_api_auth_user, users):
    url = resolve_url(URL, pk=404)

    resp = client_api_auth_user.get(url)

    assert resp.status_code == status.HTTP_404_NOT_FOUND

    body = resp.json()

    assert body["detail"] == "Não encontrado."


def test_negative_inactive_must_return_404(client_api_auth_user, pets):
    pk = Pet.objects.filter(is_active=False).values_list("pk").first()[0]

    url = resolve_url(URL, pk=pk)

    resp = client_api_auth_user.get(url)

    assert resp.status_code == status.HTTP_404_NOT_FOUND

    body = resp.json()

    assert body["detail"] == "Não encontrado."


def test_negative_must_be_auth(client_api, users):
    url = resolve_url(URL, pk=1)

    resp = client_api.get(url)

    assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    body = resp.json()

    assert body["detail"] == "As credenciais de autenticação não foram fornecidas."
