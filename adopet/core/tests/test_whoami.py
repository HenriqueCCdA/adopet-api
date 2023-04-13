import pytest
from django.shortcuts import resolve_url
from rest_framework import status

pytestmark = pytest.mark.django_db


URL = "core:whoami"


def test_positive_whoami_tutor(client_api_auth_tutor, tutor):
    url = resolve_url(URL)

    resp = client_api_auth_tutor.get(url)
    assert resp.status_code == status.HTTP_200_OK

    body = resp.json()

    assert body == {
        "id": tutor.pk,
        "name": tutor.name,
        "email": tutor.email,
        "role": "tutor",
    }


def test_positive_whoami_shelter(client_api_auth_shelter, shelter):
    url = resolve_url(URL)

    resp = client_api_auth_shelter.get(url)
    assert resp.status_code == status.HTTP_200_OK

    body = resp.json()

    assert body == {
        "id": shelter.pk,
        "name": shelter.name,
        "email": shelter.email,
        "role": "shelter",
    }


def test_positive_whoami_no_shelter_or_tutor(client_api_auth_user, user):
    url = resolve_url(URL)

    resp = client_api_auth_user.get(url)
    assert resp.status_code == status.HTTP_200_OK

    body = resp.json()

    assert body == {
        "id": user.pk,
        "name": user.name,
        "email": user.email,
        "role": None,
    }


def test_negative_without_token(client_api):
    url = resolve_url(URL)

    resp = client_api.get(url)
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    body = resp.json()

    assert body["detail"] == "As credenciais de autenticação não foram fornecidas."
