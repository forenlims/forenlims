import pytest
from django.db import IntegrityError

from accounts.models import CustomUser
from accounts.tests.factories import (
    CustomUserFactory,
    StaffUserFactory,
    SuperUserFactory,
)


@pytest.mark.django_db
class TestCustomUserManager:
    """Test CustomUserManager methods."""

    def test_create_user_with_valid_email(self) -> None:
        """Creating a user with valid email should succeed."""
        user = CustomUser.objects.create_user(
            email='test@example.com',
            password='securepass123'
        )
        assert user.email == 'test@example.com'
        assert user.check_password('securepass123')
        assert user.is_active
        assert not user.is_staff
        assert not user.is_superuser

    def test_create_user_without_email_raises_error(self) -> None:
        """Creating a user without email should raise ValueError."""
        with pytest.raises(ValueError, match='The Email field must be set'):
            CustomUser.objects.create_user(email='', password='pass123')

    def test_create_user_with_none_email_raises_error(self) -> None:
        """Creating a user with None as email should raise ValueError."""
        with pytest.raises(ValueError, match='The Email field must be set'):
            CustomUser.objects.create_user(email=None, password='pass123')

    def test_create_user_normalizes_email(self) -> None:
        """Email should be normalized (lowercase domain)."""
        user = CustomUser.objects.create_user(
            email='test@EXAMPLE.COM',
            password='pass123'
        )
        assert user.email == 'test@example.com'

    def test_create_user_with_extra_fields(self) -> None:
        """Creating user with extra fields should work."""
        user = CustomUser.objects.create_user(
            email='test@example.com',
            password='pass123',
            first_name='John',
            last_name='Doe'
        )
        assert user.first_name == 'John'
        assert user.last_name == 'Doe'

    def test_create_superuser(self) -> None:
        """Creating superuser should set staff and superuser flags."""
        admin = CustomUser.objects.create_superuser(
            email='admin@example.com',
            password='adminpass123'
        )
        assert admin.is_staff
        assert admin.is_superuser
        assert admin.is_active

    def test_create_superuser_with_extra_fields(self) -> None:
        """Superuser creation should accept extra fields."""
        admin = CustomUser.objects.create_superuser(
            email='admin@example.com',
            password='adminpass123',
            first_name='Admin',
            last_name='User'
        )
        assert admin.first_name == 'Admin'
        assert admin.last_name == 'User'


@pytest.mark.django_db
class TestCustomUserModel:
    """Test CustomUser model behavior."""

    def test_user_str_representation(self) -> None:
        """String representation should be the email."""
        user = CustomUserFactory(email='test@example.com')
        assert str(user) == 'test@example.com'

    def test_email_must_be_unique(self) -> None:
        """Duplicate emails should raise IntegrityError."""
        CustomUserFactory(email='duplicate@example.com')
        with pytest.raises(IntegrityError):
            CustomUserFactory(email='duplicate@example.com')

    def test_user_has_username_field_set_to_email(self) -> None:
        """USERNAME_FIELD should be email."""
        assert CustomUser.USERNAME_FIELD == 'email'

    def test_user_required_fields_is_empty(self) -> None:
        """REQUIRED_FIELDS should be empty (only email needed)."""
        assert CustomUser.REQUIRED_FIELDS == []

    def test_password_is_hashed(self) -> None:
        """Password should be stored hashed, not in plaintext."""
        user = CustomUserFactory(password='mypassword123')
        assert user.password != 'mypassword123'
        assert user.check_password('mypassword123')

    def test_inactive_user_creation(self) -> None:
        """Can create inactive users."""
        user = CustomUserFactory(is_active=False)
        assert not user.is_active

    def test_user_has_date_joined(self) -> None:
        """User should have date_joined set automatically."""
        user = CustomUserFactory()
        assert user.date_joined is not None


@pytest.mark.django_db
class TestUserFactories:
    """Test that factories work correctly."""

    def test_custom_user_factory_creates_valid_user(self) -> None:
        """CustomUserFactory should create a valid user."""
        user = CustomUserFactory()
        assert user.email
        assert user.first_name
        assert user.last_name
        assert user.is_active
        assert not user.is_staff
        assert not user.is_superuser
        assert user.check_password('defaultpass123')

    def test_custom_user_factory_with_custom_password(self) -> None:
        """Factory should accept custom password."""
        user = CustomUserFactory(password='custompass456')
        assert user.check_password('custompass456')

    def test_staff_user_factory_creates_staff(self) -> None:
        """StaffUserFactory should create staff user."""
        user = StaffUserFactory()
        assert user.is_staff
        assert not user.is_superuser

    def test_superuser_factory_creates_superuser(self) -> None:
        """SuperUserFactory should create superuser."""
        user = SuperUserFactory()
        assert user.is_staff
        assert user.is_superuser

    def test_factory_creates_unique_emails(self) -> None:
        """Multiple factory calls should create unique emails."""
        user1 = CustomUserFactory()
        user2 = CustomUserFactory()
        assert user1.email != user2.email

    def test_factory_batch_creation(self) -> None:
        """Factory should support batch creation."""
        users = CustomUserFactory.create_batch(5)
        assert len(users) == 5
        emails = {user.email for user in users}
        assert len(emails) == 5  # All unique
