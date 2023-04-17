import pytest
from django.contrib.auth import get_user_model
from django.shortcuts import resolve_url
from rest_framework import status

pytestmark = pytest.mark.django_db

User = get_user_model()


URL = "core:read-delete-update-shelter"


def test_positive_by_id(client_api_auth_shelter, shelter):
    """Sotf delete: return 200 and a msg."""

    pk = shelter.pk

    url = resolve_url(URL, pk=pk)

    resp = client_api_auth_shelter.delete(url)

    assert resp.status_code == status.HTTP_200_OK

    shelter.refresh_from_db()

    body = resp.json()

    assert body["msg"] == "Abrigo deletado com sucesso."
    assert not shelter.is_active


def test_negative_only_own_shelter_can_delete_itself(client_api_auth_shelter, shelter, users):
    pk = User.objects.shelter().exclude(id=shelter.pk).values_list("pk").first()[0]

    url = resolve_url(URL, pk=pk)

    resp = client_api_auth_shelter.delete(url)

    assert resp.status_code == status.HTTP_403_FORBIDDEN

    shelter.refresh_from_db()

    body = resp.json()

    assert body["detail"] == "Você não tem permissão para executar essa ação."
    assert shelter.is_active


def test_negative_invalid_id(client_api_auth_shelter, users):
    """Wrong id must return 404"""

    url = resolve_url(URL, pk=404)

    resp = client_api_auth_shelter.delete(url)

    assert resp.status_code == status.HTTP_404_NOT_FOUND

    body = resp.json()

    assert body["detail"] == "Não encontrado."


def test_negative_shelter_inactive_must_return_404(client_api_auth_shelter, users):
    """Inactive shelter must return 404"""

    pk = User.objects.filter(is_active=False, is_tutor=False, is_shelter=True).values_list("pk").first()[0]

    url = resolve_url(URL, pk=pk)

    resp = client_api_auth_shelter.delete(url)

    assert resp.status_code == status.HTTP_404_NOT_FOUND

    body = resp.json()

    assert body["detail"] == "Não encontrado."


def test_negative_must_be_auth(client_api, users):
    url = resolve_url(URL, pk=1)

    resp = client_api.delete(url)

    assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    body = resp.json()

    assert body["detail"] == "As credenciais de autenticação não foram fornecidas."
