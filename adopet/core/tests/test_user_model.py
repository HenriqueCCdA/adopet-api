from datetime import datetime

import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

pytestmark = pytest.mark.django_db


@pytest.fixture
def user():
    return User.objects.create_user(email="teste@email.com", password="123456")


def test_positive_create_user(user):
    assert user.pk
    assert User.objects.exists()


def test_positive_create_superuser():
    user = User.objects.create_superuser(email="teste@email.com", password="123456")
    assert user.is_staff
    assert user.is_superuser
    assert not user.is_tutor


def test_positive_default(user):
    assert not user.is_staff
    assert user.is_active
    assert not user.is_tutor


def test_create_at_and_modified_at(user):
    assert isinstance(user.created_at, datetime)
    assert isinstance(user.modified_at, datetime)


def test_str(user):
    assert str(user) == user.email
