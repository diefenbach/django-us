from django.contrib.auth.models import Permission
import pytest


# Fixture tests
@pytest.mark.django_db
@pytest.mark.fixture_test
def test_user_fixture(user):
    assert user.username == "doe"
    assert user.has_perm("us.add_url") is False

    add_url = Permission.objects.get(codename="add_url")
    user.user_permissions.add(add_url)

    delattr(user, "_perm_cache")  # wtf?
    assert user.has_perm("us.add_url") is True


@pytest.mark.django_db
@pytest.mark.fixture_test
def test_user_with_perm_fixture(user_with_perm):
    assert user_with_perm.username == "doe"
    assert user_with_perm.has_perm("us.add_url") is True


@pytest.mark.fixture_test
def test_get_request(gr):
    assert gr.method == "GET"
