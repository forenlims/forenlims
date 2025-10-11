"""
Pytest fixtures for accounts app tests.

Fixtures are reusable test setup objects that are automatically
injected into tests when used as parameters.
"""
import pytest
from django.test import Client

from accounts.models import CustomUser
from accounts.tests.factories import (
    CustomUserFactory,
    StaffUserFactory,
    SuperUserFactory,
)

# ============================================================================
# USER FIXTURES
# Create user objects that can be used in tests
# ============================================================================

@pytest.fixture
def user() -> CustomUser:
    """
    Fixture for a regular user.

    Usage in tests:
        def test_something(user):
            assert user.email
    """
    return CustomUserFactory()


@pytest.fixture
def staff_user() -> CustomUser:
    """
    Fixture for a staff user (has access to admin).

    Usage in tests:
        def test_admin_access(staff_user):
            assert staff_user.is_staff
    """
    return StaffUserFactory()


@pytest.fixture
def superuser() -> CustomUser:
    """
    Fixture for a superuser (has all permissions).

    Usage in tests:
        def test_superuser_permissions(superuser):
            assert superuser.is_superuser
    """
    return SuperUserFactory()


# ============================================================================
# CLIENT FIXTURES
# Django's TestClient simulates HTTP requests (like a browser).
# These fixtures create clients that are already logged in.
# ============================================================================

@pytest.fixture
def authenticated_client(user: CustomUser) -> Client:
    """
    A TestClient authenticated as a regular user.

    Usage in tests:
        def test_logged_in_view(authenticated_client):
            response = authenticated_client.get('/profile/')
            assert response.status_code == 200

    Why? Saves you from repeating in every test:
        client = Client()
        client.force_login(user)
    """
    client = Client()
    client.force_login(user)
    return client


@pytest.fixture
def staff_client(staff_user: CustomUser) -> Client:
    """
    A TestClient authenticated as a staff user.

    Usage in tests:
        def test_admin_page(staff_client):
            response = staff_client.get('/admin/')
            assert response.status_code == 200
    """
    client = Client()
    client.force_login(staff_user)
    return client


@pytest.fixture
def admin_client(superuser: CustomUser) -> Client:
    """
    A TestClient authenticated as a superuser.

    Usage in tests:
        def test_admin_delete(admin_client):
            response = admin_client.post('/admin/delete/123/')
            assert response.status_code == 302
    """
    client = Client()
    client.force_login(superuser)
    return client
