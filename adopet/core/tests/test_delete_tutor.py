import pytest
from django.contrib.auth import get_user_model
from django.shortcuts import resolve_url
from rest_framework import status

pytestmark = pytest.mark.django_db

User = get_user_model()


URL = "core:read-delete-update-tutor"


def test_positive_get_by_id(client_api, users):
    tutor = User.objects.filter(is_active=True).first()

    pk = tutor.pk

    url = resolve_url(URL, pk=pk)

    resp = client_api.delete(url)

    assert resp.status_code == status.HTTP_200_OK
    tutor = User.objects.get(pk=pk)
    body = resp.json()

    assert body["msg"] == "Tutor deletado com sucesso."
    assert not tutor.is_active


def test_negative_invalid_id(client_api, users):
    url = resolve_url(URL, pk=404)

    resp = client_api.delete(url)

    assert resp.status_code == status.HTTP_404_NOT_FOUND

    body = resp.json()

    assert body["detail"] == "Not found."


def test_negative_tutor_inactive_must_return_404(client_api, users):
    pk = User.objects.filter(is_active=False).values_list("pk").first()[0]

    url = resolve_url(URL, pk=pk)

    resp = client_api.delete(url)

    assert resp.status_code == status.HTTP_404_NOT_FOUND

    body = resp.json()

    assert body["detail"] == "Not found."
