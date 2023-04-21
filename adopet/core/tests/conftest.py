import io

import pytest
from django.core.files.base import ContentFile
from model_bakery import baker
from PIL import Image

from adopet.accounts.models import CustomUser as User
from adopet.conftest import fake
from adopet.core.models import Adoption, Pet

pytestmark = pytest.mark.django_db


@pytest.fixture
def pet_photo():
    file = io.BytesIO()
    image = Image.new("RGBA", size=(100, 100), color=(155, 0, 0))
    image.save(file, "png")
    file.seek(0)
    return ContentFile(file.read(), name="photo.png")


@pytest.fixture
def shelter():
    return baker.make(User, role=User.Role.SHELTER, is_active=True)


@pytest.fixture
def tutor():
    return baker.make(User, role=User.Role.TUTOR, is_active=True)


@pytest.fixture
def pet(shelter, pet_photo):
    return baker.make(Pet, shelter=shelter, photo=pet_photo)


@pytest.fixture
def pets(shelter, pet_photo):
    baker.make(Pet, _quantity=4, shelter=shelter, photo=pet_photo)
    baker.make(Pet, _quantity=2, is_adopted=True, shelter=shelter, photo=pet_photo)
    baker.make(Pet, _quantity=3, is_active=False, shelter=shelter, photo=pet_photo)

    return list(Pet.objects.all())


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
        "shelter": shelter.pk,
        "photo": pet_photo,
    }


@pytest.fixture
def create_adoption_payload(pet, tutor):
    return {
        "pet": pet.pk,
        "tutor": tutor.pk,
        "date": "2011-04-01",
    }
