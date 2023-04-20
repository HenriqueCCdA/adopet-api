import pytest
from django.contrib.auth import get_user_model
from django.shortcuts import resolve_url
from rest_framework import status

pytestmark = pytest.mark.django_db

User = get_user_model()


URL = "core:list-create-shelter"


def test_positive_list(client_api_auth_shelter, users):
    """
    Shelter list. Return 200.
    """

    url = resolve_url(URL)

    resp = client_api_auth_shelter.get(url)

    assert resp.status_code == status.HTTP_200_OK

    shelters = User.objects.shelter()

    body = resp.json()

    assert body["count"] == len(shelters)
    assert body["next"] is None
    assert body["previous"] is None

    for r, db in zip(body["results"], shelters):
        assert r["id"] == db.id
        assert r["name"] == db.name
        assert r["email"] == db.email
        assert r["role"] == "S"
        assert r["is_active"]
        assert r["url"] == f"http://testserver/abrigos/{db.pk}/"
        assert r["created_at"] == str(db.created_at.astimezone().isoformat())
        assert r["modified_at"] == str(db.modified_at.astimezone().isoformat())


# TODO: implementar isso depois
@pytest.mark.skip
def test_positive_list_empty(client_api_auth_shelter):
    url = resolve_url(URL)

    resp = client_api_auth_shelter.get(url)

    assert resp.status_code == status.HTTP_200_OK

    body = resp.json()

    assert body["detail"] == "Não encontrado"


def test_positive_pagination(client_api_auth_shelter, users):
    """
    Shelter list pagination. Return 200.
    """

    url = resolve_url(URL)

    resp = client_api_auth_shelter.get(f"{url}?page=2&page_size=2")

    assert resp.status_code == status.HTTP_200_OK

    shelters = User.objects.shelter()[2:4]

    body = resp.json()

    assert body["count"] == 7
    assert body["next"] == "http://testserver/abrigos/?page=3&page_size=2"
    assert body["previous"] == "http://testserver/abrigos/?page_size=2"

    for r, db in zip(body["results"], shelters):
        assert r["id"] == db.id
        assert r["name"] == db.name
        assert r["email"] == db.email
        assert r["url"] == f"http://testserver/abrigos/{db.pk}/"
        assert r["role"] == "S"
        assert r["is_active"]
        assert r["created_at"] == str(db.created_at.astimezone().isoformat())
        assert r["modified_at"] == str(db.modified_at.astimezone().isoformat())


def test_negative_invalid_page_pagination(client_api_auth_shelter, users):
    """
    Página inválida. Return 404 and 'Invalid page'.
    """

    url = resolve_url(URL)

    resp = client_api_auth_shelter.get(f"{url}?page=5")

    assert resp.status_code == status.HTTP_404_NOT_FOUND

    body = resp.json()

    assert body["detail"] == "Página inválida."


def test_negative_must_be_auth(client_api, users):
    url = resolve_url(URL)

    resp = client_api.get(url)

    assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    body = resp.json()

    assert body["detail"] == "As credenciais de autenticação não foram fornecidas."
