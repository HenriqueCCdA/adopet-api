import pytest
from model_bakery import baker

from adopet.conftest import fake
from adopet.core.models import CustomUser as User
from adopet.pet.models import Pet

pytestmark = pytest.mark.django_db


@pytest.fixture
def shelter():
    return baker.make(User, is_shelter=True, is_active=True)


@pytest.fixture
def pet(shelter):
    return baker.make(Pet, shelter=shelter)


@pytest.fixture
def pets(shelter):
    baker.make(Pet, _quantity=4, shelter=shelter)
    baker.make(Pet, _quantity=2, is_adopted=True, shelter=shelter)
    baker.make(Pet, _quantity=3, is_active=False, shelter=shelter)

    return list(Pet.objects.all())


@pytest.fixture
def create_pet_payload(shelter):
    return {
        "name": fake.name(),
        "size": "B",
        "age": 2,
        "behavior": fake.sentence(nb_words=5),
        "shelter": shelter.pk,
    }
