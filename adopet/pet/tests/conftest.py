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


@pytest.fixture
def pets(shelter):
    return baker.make(Pet, _quantity=4, shelter=shelter)
