import pytest
from model_bakery import baker

from adopet.conftest import fake
from adopet.core.models import Adoption, Pet

pytestmark = pytest.mark.django_db


@pytest.fixture
def adoption(pet, tutor):
    return baker.make(Adoption, pet=pet, tutor=tutor)


@pytest.fixture
def outher_adoption(pet_from_other_shelter, tutor):
    return baker.make(Adoption, pet=pet_from_other_shelter, tutor=tutor)


@pytest.fixture
def adoptions(shelter, other_shelter, tutor, other_tutor):
    for _ in range(2):
        pet = baker.make(Pet, shelter=shelter)
        baker.make(Adoption, pet=pet, tutor=tutor)

        pet = baker.make(Pet, shelter=other_shelter)
        baker.make(Adoption, pet=pet, tutor=other_tutor)


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
