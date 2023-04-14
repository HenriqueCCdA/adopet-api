from unittest.mock import MagicMock

import pytest
from django.contrib.auth.models import AnonymousUser

from adopet.core.authentication import RegisterAuthenticated
from adopet.core.models import CustomUser


def test_positive_post():
    request = MagicMock(method="POST", user=AnonymousUser())
    permission = RegisterAuthenticated()

    assert permission.has_permission(request, None)


@pytest.mark.parametrize("method", ["GET", "PUT", "DELETE", "PATCH"])
def test_positive_method(method):
    request = MagicMock(method=method, user=CustomUser())
    permission = RegisterAuthenticated()

    assert permission.has_permission(request, None)


@pytest.mark.parametrize("method", ["GET", "PUT", "DELETE", "PATCH"])
def test_negative_method(method):
    request = MagicMock(method=method, user=AnonymousUser())
    permission = RegisterAuthenticated()

    assert not permission.has_permission(request, None)
