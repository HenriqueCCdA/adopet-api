import pytest
from django.contrib.auth import get_user_model
from django.shortcuts import resolve_url
from rest_framework import status

pytestmark = pytest.mark.django_db

User = get_user_model()


URL = "core:list-tutor"


def test_positive_list(client_api, users):
    url = resolve_url(URL)

    resp = client_api.get(url)

    assert resp.status_code == status.HTTP_200_OK

    tutors = User.objects.filter(is_tutor=True, is_active=True)

    body = resp.json()

    assert body["count"] == 5
    assert body["next"] is None
    assert body["previous"] is None

    for r, db in zip(body["results"], tutors):
        assert r["id"] == db.id
        assert r["name"] == db.name
        assert r["email"] == db.email
        assert r["created_at"] == str(db.created_at.astimezone().isoformat())
        assert r["modified_at"] == str(db.modified_at.astimezone().isoformat())


def test_positive_pagination(client_api, users):
    url = resolve_url(URL)

    resp = client_api.get(f"{url}?page=2&page_size=2")

    assert resp.status_code == status.HTTP_200_OK

    tutors = User.objects.filter(is_tutor=True, is_active=True)[2:4]

    body = resp.json()

    assert body["count"] == 5
    assert body["next"] == "http://testserver/tutores/?page=3&page_size=2"
    assert body["previous"] == "http://testserver/tutores/?page_size=2"

    for r, db in zip(body["results"], tutors):
        assert r["id"] == db.id
        assert r["name"] == db.name
        assert r["email"] == db.email
        assert r["created_at"] == str(db.created_at.astimezone().isoformat())
        assert r["modified_at"] == str(db.modified_at.astimezone().isoformat())


def test_negative_invalid_page_pagination(client_api, users):
    url = resolve_url(URL)

    resp = client_api.get(f"{url}?page=5")

    assert resp.status_code == status.HTTP_404_NOT_FOUND

    body = resp.json()

    assert body["detail"] == "Invalid page."
