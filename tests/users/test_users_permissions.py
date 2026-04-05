from rest_framework.test import APIRequestFactory

from users.api.admin.permissions import IsAdminUserRole
from users.api.permissions import IsClientUser, IsSpecialistUser


def test_is_client_user_allows_client(client_user):
    request = APIRequestFactory().get("/fake/")
    request.user = client_user

    assert IsClientUser().has_permission(request, view=None) is True


def test_is_client_user_denies_specialist(specialist_user):
    request = APIRequestFactory().get("/fake/")
    request.user = specialist_user

    assert IsClientUser().has_permission(request, view=None) is False


def test_is_specialist_user_allows_specialist(specialist_user):
    request = APIRequestFactory().get("/fake/")
    request.user = specialist_user

    assert IsSpecialistUser().has_permission(request, view=None) is True


def test_is_specialist_user_denies_client(client_user):
    request = APIRequestFactory().get("/fake/")
    request.user = client_user

    assert IsSpecialistUser().has_permission(request, view=None) is False


def test_is_admin_user_role_allows_employee(employee_user):
    request = APIRequestFactory().get("/fake/")
    request.user = employee_user

    assert IsAdminUserRole().has_permission(request, view=None) is True


def test_is_admin_user_role_allows_superuser(superuser):
    request = APIRequestFactory().get("/fake/")
    request.user = superuser

    assert IsAdminUserRole().has_permission(request, view=None) is True


def test_is_admin_user_role_allows_owner_specialist(owner_specialist_user):
    request = APIRequestFactory().get("/fake/")
    request.user = owner_specialist_user

    assert IsAdminUserRole().has_permission(request, view=None) is True


def test_is_admin_user_role_denies_client(client_user):
    request = APIRequestFactory().get("/fake/")
    request.user = client_user

    assert IsAdminUserRole().has_permission(request, view=None) is False


def test_is_admin_user_role_denies_regular_specialist(specialist_user):
    request = APIRequestFactory().get("/fake/")
    request.user = specialist_user

    assert IsAdminUserRole().has_permission(request, view=None) is False
