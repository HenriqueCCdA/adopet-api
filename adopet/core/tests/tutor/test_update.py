import pytest
from django.contrib.auth import get_user_model
from django.shortcuts import resolve_url
from rest_framework import status

pytestmark = pytest.mark.django_db

User = get_user_model()


URL = "core:read-delete-update-tutor"


def test_positive(client_api_auth_tutor, tutor):
    pk = tutor.pk

    data = {"name": "Update name"}

    url = resolve_url(URL, pk=pk)

    resp = client_api_auth_tutor.patch(url, data=data)

    assert resp.status_code == status.HTTP_200_OK
    body = resp.json()

    assert body["name"] == "Update name"


def test_negative_only_own_tutor_can_update_itself(client_api_auth_tutor, tutor, users):
    pk = User.objects.tutor().exclude(id=tutor.pk).values_list("pk").first()[0]

    url = resolve_url(URL, pk=pk)

    resp = client_api_auth_tutor.patch(url)

    assert resp.status_code == status.HTTP_403_FORBIDDEN

    body = resp.json()

    assert body["detail"] == "Você não tem permissão para executar essa ação."


def test_negative_invalid_id(client_api_auth_tutor, users):
    url = resolve_url(URL, pk=444444)

    resp = client_api_auth_tutor.patch(url)

    assert resp.status_code == status.HTTP_404_NOT_FOUND

    body = resp.json()

    assert body["detail"] == "Não encontrado."


def test_negative_tutor_inactive_must_return_404(client_api_auth_tutor, users):
    pk = User.objects.filter(is_active=False, role=User.Role.TUTOR).values_list("pk").first()[0]

    url = resolve_url(URL, pk=pk)

    resp = client_api_auth_tutor.patch(url)

    assert resp.status_code == status.HTTP_404_NOT_FOUND

    body = resp.json()

    assert body["detail"] == "Não encontrado."


def test_negative_email_must_be_unique(client_api_auth_tutor, tutor, users):
    pk = tutor.pk

    other_tutor_email = User.objects.tutor().exclude(id=tutor.pk).values_list("email").last()[0]

    url = resolve_url(URL, pk=pk)

    data = {"email": other_tutor_email}

    resp = client_api_auth_tutor.patch(url, data=data)

    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    body = resp.json()

    assert body["email"] == ["usuário com este Email já existe."]


def test_negative_invalid_email(client_api_auth_tutor, tutor):
    pk = tutor.pk

    url = resolve_url(URL, pk=pk)

    data = {"email": "invalid@"}

    resp = client_api_auth_tutor.patch(url, data=data)

    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    body = resp.json()

    assert body["email"] == ["Insira um endereço de email válido."]


def test_negative_put_is_not_allowed(client_api_auth_tutor, users):
    pk = User.objects.tutor().values_list("pk").first()[0]

    url = resolve_url(URL, pk=pk)

    resp = client_api_auth_tutor.put(url)

    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    body = resp.json()

    assert body["detail"] == 'Method "PUT" not allowed.'


def test_negative_must_be_auth(client_api, users):
    url = resolve_url(URL, pk=1)

    resp = client_api.patch(url)

    assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    body = resp.json()

    assert body["detail"] == "As credenciais de autenticação não foram fornecidas."
