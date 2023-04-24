import pytest
from django.shortcuts import resolve_url
from rest_framework import status

from adopet.core.models import Adoption

pytestmark = pytest.mark.django_db


URL = "core:list-create-adoption"


def test_positive_list_only_adoptions_related_to_the_auth_shelter(client_api_auth_shelter, adoptions, shelter):
    url = resolve_url(URL)

    resp = client_api_auth_shelter.get(url)

    assert resp.status_code == status.HTTP_200_OK

    body = resp.json()

    assert body["count"] == 2
    assert body["next"] is None
    assert body["previous"] is None

    adoption = Adoption.objects.filter(pet__shelter=shelter, is_active=True)

    for r, db in zip(body["results"], adoption):
        assert r["id"] == db.id
        assert r["pet"] == db.pet.pk
        assert r["tutor"] == db.tutor.pk
        assert r["date"] == str(db.date)
        assert r["created_at"] == str(db.created_at.astimezone().isoformat())
        assert r["modified_at"] == str(db.modified_at.astimezone().isoformat())


def test_positive_list_only_adoptions_related_to_the_auth_tutor(client_api_auth_tutor, adoptions, tutor):
    url = resolve_url(URL)

    resp = client_api_auth_tutor.get(url)

    assert resp.status_code == status.HTTP_200_OK

    body = resp.json()

    assert body["count"] == 2
    assert body["next"] is None
    assert body["previous"] is None

    adoption = Adoption.objects.filter(tutor=tutor, is_active=True)

    for r, db in zip(body["results"], adoption):
        assert r["id"] == db.id
        assert r["pet"] == db.pet.pk
        assert r["tutor"] == db.tutor.pk
        assert r["date"] == str(db.date)
        assert r["created_at"] == str(db.created_at.astimezone().isoformat())
        assert r["modified_at"] == str(db.modified_at.astimezone().isoformat())


def test_negative_invalid_page_pagination(client_api_auth_shelter, adoptions):
    url = resolve_url(URL)

    resp = client_api_auth_shelter.get(f"{url}?page=5")

    assert resp.status_code == status.HTTP_404_NOT_FOUND

    body = resp.json()

    assert body["detail"] == "Página inválida."


def test_negative_must_be_auth(client_api, adoptions):
    url = resolve_url(URL)

    resp = client_api.get(url)

    assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    body = resp.json()

    assert body["detail"] == "As credenciais de autenticação não foram fornecidas."
