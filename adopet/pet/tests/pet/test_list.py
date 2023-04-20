import pytest
from django.shortcuts import resolve_url
from rest_framework import status

from adopet.pet.models import Pet

pytestmark = pytest.mark.django_db


URL = "pet:list-create-pet"


def test_positive_list(client_api_auth_user, pets):
    url = resolve_url(URL)

    resp = client_api_auth_user.get(url)

    assert resp.status_code == status.HTTP_200_OK

    body = resp.json()

    assert body["count"] == 6
    assert body["next"] is None
    assert body["previous"] is None

    for r, db in zip(body["results"], Pet.objects.filter(is_active=True)):
        assert r["id"] == db.id
        assert r["name"] == db.name
        assert r["size"] == db.size
        assert r["age"] == db.age
        assert r["behavior"] == db.behavior
        assert r["photo"] == "http://testserver" + db.photo.url
        assert r["shelter"] == db.shelter.pk
        assert r["is_adopted"] == db.is_adopted
        assert r["created_at"] == str(db.created_at.astimezone().isoformat())
        assert r["modified_at"] == str(db.modified_at.astimezone().isoformat())


def test_positive_pagination(client_api_auth_user, pets):
    url = resolve_url(URL)

    resp = client_api_auth_user.get(f"{url}?page=2&page_size=2")

    assert resp.status_code == status.HTTP_200_OK

    pets_ = Pet.objects.filter(is_active=True)[2:4]

    body = resp.json()

    assert body["count"] == 6
    assert body["next"] == "http://testserver/pet/?page=3&page_size=2"
    assert body["previous"] == "http://testserver/pet/?page_size=2"

    for r, db in zip(body["results"], pets_):
        assert r["id"] == db.id
        assert r["name"] == db.name
        assert r["size"] == db.size
        assert r["age"] == db.age
        assert r["behavior"] == db.behavior
        assert r["photo"] == "http://testserver" + db.photo.url
        assert r["shelter"] == db.shelter.pk
        assert r["is_adopted"] == db.is_adopted
        assert r["created_at"] == str(db.created_at.astimezone().isoformat())
        assert r["modified_at"] == str(db.modified_at.astimezone().isoformat())


def test_negative_invalid_page_pagination(client_api_auth_user, pets):
    url = resolve_url(URL)

    resp = client_api_auth_user.get(f"{url}?page=5")

    assert resp.status_code == status.HTTP_404_NOT_FOUND

    body = resp.json()

    assert body["detail"] == "Página inválida."


def test_negative_must_be_auth(client_api, users):
    url = resolve_url(URL)

    resp = client_api.get(url)

    assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    body = resp.json()

    assert body["detail"] == "As credenciais de autenticação não foram fornecidas."
