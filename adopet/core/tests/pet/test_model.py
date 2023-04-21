from datetime import datetime

import pytest

from adopet.core.models import Pet

pytestmark = pytest.mark.django_db


def test_positive_create(pet):
    assert pet.pk
    assert Pet.objects.exists()


def test_positive_default(pet):
    assert pet.is_active
    assert not pet.is_adopted


def test_create_at_and_modified_at(pet):
    assert isinstance(pet.created_at, datetime)
    assert isinstance(pet.modified_at, datetime)


def test_str(pet):
    assert str(pet) == pet.name


def test_relations(pets, shelter):
    assert pets[0].shelter == shelter

    assert shelter.pets.count() == 9
    assert shelter.pets.last() == pets[-1]
