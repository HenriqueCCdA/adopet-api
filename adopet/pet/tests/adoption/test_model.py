from datetime import datetime

import pytest

from adopet.pet.models import Adoption

pytestmark = pytest.mark.django_db


def test_positive_create(adoption):
    assert adoption.pk
    assert adoption.pet
    assert adoption.tutor
    assert adoption.date
    assert Adoption.objects.exists()


def test_positive_default(adoption):
    assert adoption.is_active


def test_create_at_and_modified_at(adoption):
    assert isinstance(adoption.created_at, datetime)
    assert isinstance(adoption.modified_at, datetime)


def test_str(adoption):
    assert str(adoption) == f"{adoption.tutor.name}:{adoption.pet}"


def test_relations(adoption, pet, tutor):
    assert adoption.tutor == tutor
    assert adoption.pet == pet

    assert tutor.adoptions.count() == 1
    assert pet.adoption == adoption
