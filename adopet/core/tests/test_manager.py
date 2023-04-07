from adopet.core.models import CustomUser as User


def test_shelter(users):
    """
    Return only user with is_tutor=False, is_shelter=True, is_active=True
    """
    assert User.objects.shelter().count() == 6


def test_shelter_all(users):
    """
    Return only user with is_tutor=False, is_shelter=True
    """
    assert User.objects.shelter(all=True).count() == 13


def test_tutor(users):
    """
    Return only user with is_tutor=True, is_shelter=False, is_active=True
    """
    assert User.objects.tutor().count() == 5


def test_tutor_all(users):
    """
    Return only user with is_tutor=True, is_shelter=False
    """
    assert User.objects.tutor(all=True).count() == 10
