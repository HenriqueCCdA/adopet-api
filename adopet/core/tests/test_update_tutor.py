import pytest
from django.contrib.auth import get_user_model
from django.shortcuts import resolve_url
from rest_framework import status

pytestmark = pytest.mark.django_db

User = get_user_model()


URL = "core:read-delete-update-tutor"


def test_positive(client_api, users):
    tutor = User.objects.filter(is_active=True).first()

    pk = tutor.pk

    data = {"name": "Update name"}

    url = resolve_url(URL, pk=pk)

    resp = client_api.patch(url, data=data)

    assert resp.status_code == status.HTTP_200_OK
    tutor = User.objects.get(pk=pk)
    body = resp.json()

    assert body["name"] == "Update name"


def test_negative_invalid_id(client_api, users):
    url = resolve_url(URL, pk=404)

    resp = client_api.patch(url)

    assert resp.status_code == status.HTTP_404_NOT_FOUND

    body = resp.json()

    assert body["detail"] == "Not found."


def test_negative_tutor_inactive_must_return_404(client_api, users):
    pk = User.objects.filter(is_active=False).values_list("pk").first()[0]

    url = resolve_url(URL, pk=pk)

    resp = client_api.patch(url)

    assert resp.status_code == status.HTTP_404_NOT_FOUND

    body = resp.json()

    assert body["detail"] == "Not found."


def test_negative_email_mest_be_unique(client_api, users):
    pk = User.objects.filter(is_active=True).values_list("pk").first()[0]

    other_tutor_email = User.objects.filter(is_active=True).values_list("email").last()[0]

    url = resolve_url(URL, pk=pk)

    data = {"email": other_tutor_email}

    resp = client_api.patch(url, data=data)

    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    body = resp.json()

    assert body["email"] == ["usuário com este Email já existe."]


def test_negative_invalid_email(client_api, users):
    pk = User.objects.filter(is_active=True).values_list("pk").first()[0]

    url = resolve_url(URL, pk=pk)

    data = {"email": "invalid@"}

    resp = client_api.patch(url, data=data)

    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    body = resp.json()

    assert body["email"] == ["Informe um endereço de email válido."]


def test_negative_put_is_not_allowed(client_api, users):
    pk = User.objects.filter(is_active=False).values_list("pk").first()[0]

    url = resolve_url(URL, pk=pk)

    resp = client_api.put(url)

    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    body = resp.json()

    assert body["detail"] == 'Method "PUT" not allowed.'
