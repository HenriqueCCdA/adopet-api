import pytest
from django.shortcuts import resolve_url
from model_bakery import baker
from rest_framework import status

from adopet.core.models import Adoption

pytestmark = pytest.mark.django_db

URL = "core:read-delete-adoption"


def test_positive(client_api_auth_shelter, adoption):
    pk = adoption.pk
    pet = adoption.pet

    url = resolve_url(URL, pk=pk)

    resp = client_api_auth_shelter.delete(url)

    assert resp.status_code == status.HTTP_200_OK
    body = resp.json()

    assert body["msg"] == "Adoção deletada com sucesso."
    assert not Adoption.objects.exists()
    assert not pet.is_adopted


def test_negative_pet_must_belong_to_shelter(client_api_auth_shelter, pet_from_other_shelter, tutor):
    adoption = baker.make(Adoption, pet=pet_from_other_shelter, tutor=tutor)

    pk = adoption.pk
    pet = adoption.pet

    url = resolve_url(URL, pk=pk)

    resp = client_api_auth_shelter.delete(url)

    assert resp.status_code == status.HTTP_403_FORBIDDEN
    body = resp.json()

    assert body["detail"] == "Você não tem permissão para executar essa ação."
    assert Adoption.objects.exists()
    assert not pet.is_adopted


def test_negative_tutor_not_can_delete(client_api_auth_tutor, adoption):
    pk = adoption.pk

    url = resolve_url(URL, pk=pk)

    resp = client_api_auth_tutor.delete(url)

    assert resp.status_code == status.HTTP_403_FORBIDDEN
    adoption.refresh_from_db()

    assert adoption.is_active
    assert not adoption.pet.is_adopted


def test_negative_invalid_id(client_api_auth_shelter):
    url = resolve_url(URL, pk=404404)

    resp = client_api_auth_shelter.delete(url)

    assert resp.status_code == status.HTTP_404_NOT_FOUND

    body = resp.json()

    assert body["detail"] == "Não encontrado."


def test_negative_must_be_auth(client_api):
    url = resolve_url(URL, pk=1)

    resp = client_api.delete(url)

    assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    body = resp.json()

    assert body["detail"] == "As credenciais de autenticação não foram fornecidas."
