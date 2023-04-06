import pytest
from django.contrib.auth import get_user_model
from django.shortcuts import resolve_url
from rest_framework import status

pytestmark = pytest.mark.django_db

User = get_user_model()


URL = "core:list-create-shelter"


def test_positive_list(client_api, users):
    """
    Shelter list. Return 200.
    """

    url = resolve_url(URL)

    resp = client_api.get(url)

    assert resp.status_code == status.HTTP_200_OK

    tutors = User.objects.filter(is_shelter=True, is_active=True)

    body = resp.json()

    assert body["count"] == 6
    assert body["next"] is None
    assert body["previous"] is None

    for r, db in zip(body["results"], tutors):
        assert r["id"] == db.id
        assert r["name"] == db.name
        assert r["email"] == db.email
        assert not r["is_tutor"]
        assert r["is_shelter"]
        assert r["is_active"]
        assert r["url"] == f"http://testserver/abrigos/{db.pk}/"
        assert r["created_at"] == str(db.created_at.astimezone().isoformat())
        assert r["modified_at"] == str(db.modified_at.astimezone().isoformat())


# TODO: implementar isso depois
@pytest.mark.skip
def test_positive_list_empty(client_api):
    url = resolve_url(URL)

    resp = client_api.get(url)

    assert resp.status_code == status.HTTP_200_OK

    body = resp.json()

    assert body["detail"] == "Não encontrado"


def test_positive_pagination(client_api, users):
    """
    Shelter list pagination. Return 200.
    """

    url = resolve_url(URL)

    resp = client_api.get(f"{url}?page=2&page_size=2")

    assert resp.status_code == status.HTTP_200_OK

    tutors = User.objects.filter(is_shelter=True, is_active=True)[2:4]

    body = resp.json()

    assert body["count"] == 6
    assert body["next"] == "http://testserver/abrigos/?page=3&page_size=2"
    assert body["previous"] == "http://testserver/abrigos/?page_size=2"

    for r, db in zip(body["results"], tutors):
        assert r["id"] == db.id
        assert r["name"] == db.name
        assert r["email"] == db.email
        assert r["url"] == f"http://testserver/abrigos/{db.pk}/"
        assert not r["is_tutor"]
        assert r["is_shelter"]
        assert r["is_active"]
        assert r["created_at"] == str(db.created_at.astimezone().isoformat())
        assert r["modified_at"] == str(db.modified_at.astimezone().isoformat())


def test_negative_invalid_page_pagination(client_api, users):
    """
    Invalid page. Return 404 and 'Invalid page'.
    """

    url = resolve_url(URL)

    resp = client_api.get(f"{url}?page=5")

    assert resp.status_code == status.HTTP_404_NOT_FOUND

    body = resp.json()

    assert body["detail"] == "Invalid page."
