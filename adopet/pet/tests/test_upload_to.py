import pytest

from adopet.pet.models import upload_to

pytestmark = pytest.mark.django_db


def test_positive(pet):
    full_name = upload_to(pet, "photo.png")

    assert full_name == "photos/photo.png"
