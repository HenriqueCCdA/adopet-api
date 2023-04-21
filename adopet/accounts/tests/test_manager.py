from adopet.accounts.models import CustomUser as User


def test_shelter(users):
    """Return only user with role="S" and is_active=True"""
    assert User.objects.shelter().count() == 6


def test_shelter_all(users):
    """Return only user with role='S'"""
    assert User.objects.shelter(all=True).count() == 13


def test_tutor(users):
    """Return only user with role="T" and is_active=True"""
    assert User.objects.tutor().count() == 5


def test_tutor_all(users):
    """Return only user with role='T'"""
    assert User.objects.tutor(all=True).count() == 10
