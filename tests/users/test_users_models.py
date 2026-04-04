import pytest


# ==================================================
# USERS ALL
# ==================================================
def test_full_name_with_names(user_factory):
    user = user_factory(first_name="John", last_name="Doe")
    assert user.full_name == "John Doe"


def test_full_name_fallback(user_factory):
    user = user_factory(username="testuser", first_name="", last_name="")
    assert user.full_name == "testuser"


def test_user_email_field(user_factory):
    user = user_factory(email="test@example.com")
    assert user.email == "test@example.com"


# ==================================================
# CLIENT
# ==================================================
def test_client_user_created(client_user):
    assert client_user is not None


def test_client_profile_created(client_profile):
    assert client_profile is not None


def test_client_has_profile(client_user):
    assert client_user.client_profile is not None

    with pytest.raises(client_user.__class__.specialist_profile.RelatedObjectDoesNotExist):
        client_user.specialist_profile


def test_client_user_role(client_user):
    assert client_user.role == client_user.Role.CLIENT


# ==================================================
# SPECIALIST
# ==================================================
def test_specialist_user_created(specialist_user):
    assert specialist_user is not None


def test_specialist_profile_created(specialist_profile):
    assert specialist_profile is not None


def test_specialist_has_profile(specialist_user):
    assert specialist_user.specialist_profile is not None

    with pytest.raises(specialist_user.__class__.client_profile.RelatedObjectDoesNotExist):
        specialist_user.client_profile


def test_specialist_user_role(specialist_user):
    assert specialist_user.role == specialist_user.Role.SPECIALIST


# ==================================================
# EMPLOYEE
# ==================================================
def test_employee_user_created(employee_user):
    assert employee_user is not None


def test_employee_user_role(employee_user):
    assert employee_user.role == employee_user.Role.EMPLOYEE


def test_employee_has_no_profiles(employee_user):
    User = employee_user.__class__

    with pytest.raises(User.client_profile.RelatedObjectDoesNotExist):
        employee_user.client_profile

    with pytest.raises(User.specialist_profile.RelatedObjectDoesNotExist):
        employee_user.specialist_profile
