import pytest
from django.contrib.auth import get_user_model
from django.shortcuts import resolve_url
from rest_framework import status

pytestmark = pytest.mark.django_db

User = get_user_model()


URL = "core:read-delete-update-tutor"


def test_positive_get_by_id(client_api_auth_tutor, users):
    tutor = User.objects.filter(is_active=True, is_tutor=True).first()

    pk = tutor.pk

    url = resolve_url(URL, pk=pk)

    resp = client_api_auth_tutor.get(url)

    assert resp.status_code == status.HTTP_200_OK

    tutor = User.objects.get(pk=pk)
    body = resp.json()

    assert body["id"] == tutor.id
    assert body["name"] == tutor.name
    assert body["email"] == tutor.email
    assert body["is_tutor"]
    assert not body["is_shelter"]
    assert body["is_active"]
    assert body["created_at"] == str(tutor.created_at.astimezone().isoformat())
    assert body["modified_at"] == str(tutor.modified_at.astimezone().isoformat())


def test_negative_invalid_id(client_api_auth_tutor, users):
    url = resolve_url(URL, pk=404)

    resp = client_api_auth_tutor.get(url)

    assert resp.status_code == status.HTTP_404_NOT_FOUND

    body = resp.json()

    assert body["detail"] == "Não encontrado."


def test_negative_tutor_inactive_must_return_404(client_api_auth_tutor, users):
    pk = User.objects.filter(is_active=False, is_tutor=True).values_list("pk").first()[0]

    url = resolve_url(URL, pk=pk)

    resp = client_api_auth_tutor.get(url)

    assert resp.status_code == status.HTTP_404_NOT_FOUND

    body = resp.json()

    assert body["detail"] == "Não encontrado."


def test_negative_must_be_auth(client_api, users):
    url = resolve_url(URL, pk=1)

    resp = client_api.get(url)

    assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    body = resp.json()

    assert body["detail"] == "As credenciais de autenticação não foram fornecidas."
