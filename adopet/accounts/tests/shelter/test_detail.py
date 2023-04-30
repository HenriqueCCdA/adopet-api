import pytest
from django.contrib.auth import get_user_model
from django.shortcuts import resolve_url
from rest_framework import status

pytestmark = pytest.mark.django_db

User = get_user_model()


URL = "accounts:read-delete-update-shelter"


def test_positive_get_by_id(client_api_auth_shelter, users):
    shelter = User.objects.shelter().first()

    pk = shelter.pk

    url = resolve_url(URL, pk=pk)

    resp = client_api_auth_shelter.get(url)

    assert resp.status_code == status.HTTP_200_OK

    shelter = User.objects.get(pk=pk)
    body = resp.json()

    assert body["id"] == shelter.id
    assert body["name"] == shelter.name
    assert body["email"] == shelter.email
    assert body["city"] == shelter.city
    assert body["phone"] == shelter.phone
    assert body["about"] == shelter.about
    assert body["role"] == "S"
    assert body["is_active"]
    assert body["created_at"] == str(shelter.created_at.astimezone().isoformat())
    assert body["modified_at"] == str(shelter.modified_at.astimezone().isoformat())


def test_negative_invalid_id(client_api_auth_shelter, users):
    url = resolve_url(URL, pk=404)

    resp = client_api_auth_shelter.get(url)

    assert resp.status_code == status.HTTP_404_NOT_FOUND

    body = resp.json()

    assert body["detail"] == "Não encontrado."


def test_negative_inactive_must_return_404(client_api_auth_shelter, users):
    pk = User.objects.filter(is_active=False, role=User.Role.SHELTER).values_list("pk").first()[0]

    url = resolve_url(URL, pk=pk)

    resp = client_api_auth_shelter.get(url)

    assert resp.status_code == status.HTTP_404_NOT_FOUND

    body = resp.json()

    assert body["detail"] == "Não encontrado."


def test_negative_must_be_auth(client_api, users):
    url = resolve_url(URL, pk=1)

    resp = client_api.get(url)

    assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    body = resp.json()

    assert body["detail"] == "As credenciais de autenticação não foram fornecidas."
