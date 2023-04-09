from datetime import datetime

import pytest
from model_bakery import baker

from adopet.core.models import CustomUser as User
from adopet.pet.models import Pet

pytestmark = pytest.mark.django_db


@pytest.fixture
def shelter():
    return baker.make(User, is_shelter=True, is_active=False)


@pytest.fixture
def pet(shelter):
    return baker.make(Pet, shelter=shelter)


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


def test_relations(pet, shelter):
    assert pet.shelter == shelter

    assert shelter.pets.count() == 1
    assert shelter.pets.first() == pet
