import pytest
from model_bakery import baker

from adopet.conftest import fake
from adopet.core.models import Adoption

pytestmark = pytest.mark.django_db


@pytest.fixture
def adoption(pet, tutor):
    return baker.make(Adoption, pet=pet, tutor=tutor)


@pytest.fixture
def create_pet_payload(shelter, pet_photo):
    return {
        "name": fake.name(),
        "size": "B",
        "age": 2,
        "behavior": fake.sentence(nb_words=5),
        "photo": pet_photo,
    }


@pytest.fixture
def create_adoption_payload(pet, tutor):
    return {
        "pet": pet.pk,
        "tutor": tutor.pk,
        "date": "2011-04-01",
    }
