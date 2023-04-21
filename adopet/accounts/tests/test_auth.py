from unittest.mock import MagicMock

import pytest
from django.contrib.auth.models import AnonymousUser

from adopet.accounts.models import CustomUser
from adopet.accounts.permissions import RegisterPermission


def test_positive_post():
    request = MagicMock(method="POST", user=AnonymousUser())
    permission = RegisterPermission()

    assert permission.has_permission(request, None)


@pytest.mark.parametrize("method", ["GET", "PUT", "DELETE", "PATCH"])
def test_positive_method(method):
    request = MagicMock(method=method, user=CustomUser())
    permission = RegisterPermission()

    assert permission.has_permission(request, None)


@pytest.mark.parametrize("method", ["GET", "PUT", "DELETE", "PATCH"])
def test_negative_method(method):
    request = MagicMock(method=method, user=AnonymousUser())
    permission = RegisterPermission()

    assert not permission.has_permission(request, None)
