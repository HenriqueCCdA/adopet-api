import pytest
from django.contrib.auth import get_user_model
from django.shortcuts import resolve_url
from rest_framework import status

pytestmark = pytest.mark.django_db

User = get_user_model()


URL = "accounts:read-delete-update-tutor"


def test_positive_by_id(client_api_auth_tutor, tutor):
    """Sotf delete: return 200 and a msg."""

    pk = tutor.pk

    url = resolve_url(URL, pk=pk)

    resp = client_api_auth_tutor.delete(url)

    assert resp.status_code == status.HTTP_200_OK

    tutor.refresh_from_db()

    body = resp.json()

    assert body["msg"] == "Tutor deletado com sucesso."
    assert not tutor.is_active


def test_negative_only_own_tutor_can_delete_itself(client_api_auth_tutor, tutor, users):
    pk = User.objects.tutor().exclude(id=tutor.pk).values_list("pk").first()[0]

    url = resolve_url(URL, pk=pk)

    resp = client_api_auth_tutor.delete(url)

    assert resp.status_code == status.HTTP_403_FORBIDDEN

    tutor.refresh_from_db()

    body = resp.json()

    assert body["detail"] == "Você não tem permissão para executar essa ação."
    assert tutor.is_active


def test_negative_invalid_id(client_api_auth_tutor, users):
    url = resolve_url(URL, pk=404)

    resp = client_api_auth_tutor.delete(url)

    assert resp.status_code == status.HTTP_404_NOT_FOUND

    body = resp.json()

    assert body["detail"] == "Não encontrado."


def test_negative_tutor_inactive_must_return_404(client_api_auth_tutor, users):
    pk = User.objects.filter(is_active=False).values_list("pk").first()[0]

    url = resolve_url(URL, pk=pk)

    resp = client_api_auth_tutor.delete(url)

    assert resp.status_code == status.HTTP_404_NOT_FOUND

    body = resp.json()

    assert body["detail"] == "Não encontrado."


def test_negative_must_be_auth(client_api, users):
    url = resolve_url(URL, pk=1)

    resp = client_api.delete(url)

    assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    body = resp.json()

    assert body["detail"] == "As credenciais de autenticação não foram fornecidas."
