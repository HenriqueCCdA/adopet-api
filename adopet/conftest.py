import pytest
from django.contrib.auth import get_user_model
from faker import Faker
from model_bakery import baker
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

fake = Faker()

User = get_user_model()


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
    baker.make(User, _quantity=5, is_tutor=True)
    baker.make(User, _quantity=5, is_tutor=True, is_active=False)
    baker.make(User, _quantity=6, is_shelter=True)
    baker.make(User, _quantity=7, is_shelter=True, is_active=False)

    return User.objects.all()


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
def tutor():
    return User.objects.create_user(
        name=fake.name(),
        email=fake.email(),
        password=fake.password(),
        is_tutor=True,
    )


@pytest.fixture
def client_api_auth_tutor(client_api, tutor):
    token = Token.objects.create(user=tutor)

    header = {"HTTP_AUTHORIZATION": f"Token {token}"}

    client_api.credentials(**header)

    return client_api


@pytest.fixture
def shelter():
    return User.objects.create_user(
        name=fake.name(),
        email=fake.email(),
        password=fake.password(),
        is_shelter=True,
    )


@pytest.fixture
def client_api_auth_shelter(client_api, shelter):
    token = Token.objects.create(user=shelter)

    header = {"HTTP_AUTHORIZATION": f"Token {token}"}

    client_api.credentials(**header)

    return client_api


@pytest.fixture
def client_api_auth_user(client_api, user):
    token = Token.objects.create(user=user)

    header = {"HTTP_AUTHORIZATION": f"Token {token}"}

    client_api.credentials(**header)

    return client_api
