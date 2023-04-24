import io

import pytest
from django.core.files.base import ContentFile
from faker import Faker
from model_bakery import baker
from PIL import Image
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from adopet.accounts.models import CustomUser as User
from adopet.core.models import Pet

fake = Faker()


@pytest.fixture(autouse=True)
def mediafiles(settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path / "media"


@pytest.fixture
def client_api():
    return APIClient()


@pytest.fixture
def user(db):
    return baker.make(User)


@pytest.fixture
def superuser(db):
    return User.objects.create_superuser(email=fake.email(), password=fake.password())


@pytest.fixture()
def users(superuser):
    baker.make(User, _quantity=5, role=User.Role.TUTOR)
    baker.make(User, _quantity=5, role=User.Role.TUTOR, is_active=False)
    baker.make(User, _quantity=6, role=User.Role.SHELTER)
    baker.make(User, _quantity=7, role=User.Role.SHELTER, is_active=False)

    return User.objects.all()


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
def other_shelter(shelter):
    return baker.make(User, role=User.Role.SHELTER, is_active=True)


@pytest.fixture
def tutor():
    return baker.make(User, role=User.Role.TUTOR, is_active=True)


@pytest.fixture
def other_tutor(tutor):
    return baker.make(User, role=User.Role.TUTOR, is_active=True)


@pytest.fixture
def pet(shelter, pet_photo):
    return baker.make(Pet, shelter=shelter, photo=pet_photo)


@pytest.fixture
def pet_from_other_shelter(other_shelter, pet_photo):
    return baker.make(Pet, shelter=other_shelter, photo=pet_photo)


@pytest.fixture
def pets(shelter, pet_photo):
    baker.make(Pet, _quantity=4, shelter=shelter, photo=pet_photo)
    baker.make(Pet, _quantity=2, is_adopted=True, shelter=shelter, photo=pet_photo)
    baker.make(Pet, _quantity=3, is_active=False, shelter=shelter, photo=pet_photo)

    return list(Pet.objects.all())


@pytest.fixture
def create_tutor_payload():
    password = fake.password()

    return {
        "name": fake.name(),
        "email": fake.email(),
        "password": password,
        "password2": password,
    }


@pytest.fixture
def create_abrigo_payload():
    password = fake.password()

    return {
        "name": fake.name(),
        "email": fake.email(),
        "password": password,
        "password2": password,
    }


@pytest.fixture
def client_api_auth_tutor(client_api, tutor):
    token = Token.objects.create(user=tutor)

    header = {"HTTP_AUTHORIZATION": f"Bearer {token}"}

    client_api.credentials(**header)

    return client_api


@pytest.fixture
def client_api_auth_shelter(client_api, shelter):
    token = Token.objects.create(user=shelter)

    header = {"HTTP_AUTHORIZATION": f"Bearer {token}"}

    client_api.credentials(**header)

    return client_api


@pytest.fixture
def client_api_auth_user(client_api, user):
    token = Token.objects.create(user=user)

    header = {"HTTP_AUTHORIZATION": f"Bearer {token}"}

    client_api.credentials(**header)

    return client_api
