import pytest
from django.contrib.auth import get_user_model
from django.shortcuts import resolve_url
from rest_framework import status

pytestmark = pytest.mark.django_db

User = get_user_model()


URL = "core:read-delete-update-shelter"


def test_positive_by_id(client_api, users):
    """
    Sotf delete: return 200 and a msg.
    """

    shelter = User.objects.filter(is_active=True, is_tutor=False, is_shelter=True).first()

    pk = shelter.pk

    url = resolve_url(URL, pk=pk)

    resp = client_api.delete(url)

    assert resp.status_code == status.HTTP_200_OK
    shelter = User.objects.get(pk=pk)
    body = resp.json()

    assert body["msg"] == "Abrigo deletado com sucesso."
    assert not shelter.is_active


def test_negative_invalid_id(client_api, users):
    """
    Wrong id must return 404
    """

    url = resolve_url(URL, pk=404)

    resp = client_api.delete(url)

    assert resp.status_code == status.HTTP_404_NOT_FOUND

    body = resp.json()

    assert body["detail"] == "Não encontrado."


def test_negative_shelter_inactive_must_return_404(client_api, users):
    """
    Inactive shelter must return 404
    """

    pk = User.objects.filter(is_active=False, is_tutor=False, is_shelter=True).values_list("pk").first()[0]

    url = resolve_url(URL, pk=pk)

    resp = client_api.delete(url)

    assert resp.status_code == status.HTTP_404_NOT_FOUND

    body = resp.json()

    assert body["detail"] == "Não encontrado."
