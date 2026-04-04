import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def user_factory(db):
    """
    Factory for creating user with different roles.
    """

    User = get_user_model()

    def create_user(**kwargs):
        defaults = {
            "email": "client@test.com",
            "username": "client",
            "password": "testpass123",
            "role": User.Role.CLIENT,
        }
        defaults.update(kwargs)

        return User.objects.create(**defaults)

    return create_user

@pytest.fixture
def superuser(db):
    """
    Create superuser
    """
    return User.objects.create_superuser(
        email="admin@test.com",
        username="admin",
        password="adminpass123",
    )


@pytest.fixture
def client_user(user_factory):
    """
    Minimal client user.
    Profile + wallet should be created via signals.
    """
    return user_factory(role=User.Role.CLIENT)


@pytest.fixture
def client_profile(client_user):
    """
    Returns client profile created via signals.
    """
    return client_user.client_profile


@pytest.fixture
def client_wallet(client_profile):
    """
    Returns client wallet created via signal.
    """

    return client_profile.client_wallet


@pytest.fixture
def specialist_user(user_factory):
    """
    Minimal specialist user.
    Profile should be created via signals.
    """
    return user_factory(role=User.Role.SPECIALIST)


@pytest.fixture
def specialist_profile(specialist_user):
    """
    Returns specialist profile created via signals.
    """
    return specialist_user.specialist_profile


@pytest.fixture
def owner_specialist_user(specialist_user):
    """
    Specialist as Admin user.
    """
    specialist_user.specialist_profile.is_owner = True
    specialist_user.specialist_profile.save(update_fields=["is_owner"])
    return specialist_user


@pytest.fixture
def employee_user(user_factory):
    """
    Minimal employee user.
    """
    return user_factory(role=User.Role.EMPLOYEE)
