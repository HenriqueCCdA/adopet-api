import pytest
from django.contrib.auth import get_user_model
from django.shortcuts import resolve_url
from rest_framework import status

pytestmark = pytest.mark.django_db

User = get_user_model()


URL = "core:list-create-tutor"


def test_positive(client_api, create_tutor_payload):
    url = resolve_url(URL)

    resp = client_api.post(url, data=create_tutor_payload)

    assert resp.status_code == status.HTTP_201_CREATED

    tutor = User.objects.first()
    body = resp.json()

    assert body["id"] == tutor.id
    assert body["name"] == tutor.name
    assert body["email"] == tutor.email
    assert body["is_active"]
    assert body["created_at"] == str(tutor.created_at.astimezone().isoformat())
    assert body["modified_at"] == str(tutor.modified_at.astimezone().isoformat())

    assert resp["Location"] == "http://testserver/tutores/1/"

    assert tutor.check_password(create_tutor_payload["password"])


def test_negative_email_must_be_unique(client_api, create_tutor_payload):
    url = resolve_url(URL)

    resp = client_api.post(url, data=create_tutor_payload)

    assert resp.status_code == status.HTTP_201_CREATED

    resp = client_api.post(url, data=create_tutor_payload)

    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    assert User.objects.count() == 1
    body = resp.json()

    assert body == {"email": ["usuário com este Email já existe."]}


@pytest.mark.parametrize(
    "field, errors",
    [
        ("name", ["Este campo é obrigatório."]),
        ("email", ["Este campo é obrigatório."]),
        ("password", ["Este campo é obrigatório."]),
        ("password2", ["Este campo é obrigatório."]),
    ],
)
def test_negative_missing_fields(client_api, field, errors, create_tutor_payload):
    data = create_tutor_payload.copy()

    del data[field]

    url = resolve_url(URL)

    resp = client_api.post(url, data=data)

    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    assert not User.objects.exists()
    body = resp.json()

    assert body[field] == errors


@pytest.mark.parametrize(
    "password, errors",
    [
        (
            "1",
            [
                "Esta senha é muito curta. Ela precisa conter pelo menos 8 caracteres.",
                "Esta senha é muito comum.",
                "Esta senha é inteiramente numérica.",
            ],
        ),
        ("12345678", ["Esta senha é muito comum.", "Esta senha é inteiramente numérica."]),
        ("abcd1234", ["Esta senha é muito comum."]),
    ],
)
def test_negative_password_validation(client_api, password, errors, create_tutor_payload):
    data = create_tutor_payload.copy()

    data["password"] = password
    data["password2"] = password

    url = resolve_url(URL)

    resp = client_api.post(url, data=data)

    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    assert not User.objects.exists()
    body = resp.json()

    assert body["password"] == errors
