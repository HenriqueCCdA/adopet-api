import pytest
from django.shortcuts import resolve_url
from rest_framework import status

from adopet.pet.models import Pet

pytestmark = pytest.mark.django_db

URL = "pet:read-delete-update"


def test_positive_by_id(client_api_auth_user, pet):
    pk = pet.pk

    url = resolve_url(URL, pk=pk)

    resp = client_api_auth_user.delete(url)

    assert resp.status_code == status.HTTP_200_OK
    pet.refresh_from_db()
    body = resp.json()

    assert body["msg"] == "Abrigo deletado com sucesso."
    assert not pet.is_active


def test_negative_invalid_id(client_api_auth_user, pets):
    url = resolve_url(URL, pk=404404)

    resp = client_api_auth_user.delete(url)

    assert resp.status_code == status.HTTP_404_NOT_FOUND

    body = resp.json()

    assert body["detail"] == "Não encontrado."


def test_negative_tutor_inactive_must_return_404(client_api_auth_user, pets):
    pk = Pet.objects.filter(is_active=False).values_list("pk").first()[0]

    url = resolve_url(URL, pk=pk)

    resp = client_api_auth_user.delete(url)

    assert resp.status_code == status.HTTP_404_NOT_FOUND

    body = resp.json()

    assert body["detail"] == "Não encontrado."


def test_negative_must_be_auth(client_api, users):
    url = resolve_url(URL, pk=1)

    resp = client_api.delete(url)

    assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    body = resp.json()

    assert body["detail"] == "As credenciais de autenticação não foram fornecidas."
