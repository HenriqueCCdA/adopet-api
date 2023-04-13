import pytest
from django.contrib.auth import get_user_model
from django.shortcuts import resolve_url
from rest_framework import status

from adopet.conftest import fake

pytestmark = pytest.mark.django_db

User = get_user_model()

URL = "core:login"


@pytest.fixture
def login_payload():
    return {
        "username": fake.email(),
        "password": fake.password(),
    }


@pytest.fixture
def user_to_login(login_payload):
    return User.objects.create_user(email=login_payload["username"], password=login_payload["password"])


def test_positive(client_api, user_to_login, login_payload):
    url = resolve_url(URL)

    resp = client_api.post(url, data=login_payload)
    assert resp.status_code == status.HTTP_200_OK

    body = resp.json()

    user = User.objects.first()

    assert body["token"] == user.auth_token.key


def test_negative_inative_user_cannot_login(client_api, user_to_login, login_payload):
    user_to_login.is_active = False
    user_to_login.save()

    url = resolve_url(URL)

    resp = client_api.post(url, data=login_payload)
    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    body = resp.json()

    assert body["non_field_errors"] == ["Impossível fazer login com as credenciais fornecidas."]


@pytest.mark.parametrize(
    "field",
    [
        "username",
        "password",
    ],
)
def test_negative_missing_fields(client_api, field, login_payload):
    data = login_payload.copy()

    del data[field]

    url = resolve_url(URL)

    resp = client_api.post(url, data=data)
    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    body = resp.json()

    assert body[field] == ["Este campo é obrigatório."]


@pytest.mark.parametrize(
    "field",
    [
        "username",
        "password",
    ],
)
def test_negative_invalid_credentials(client_api, field, user_to_login, login_payload):
    data = login_payload.copy()

    data[field] = data[field] + "1"

    url = resolve_url(URL)

    resp = client_api.post(url, data=data)
    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    body = resp.json()

    assert body["non_field_errors"] == ["Impossível fazer login com as credenciais fornecidas."]
