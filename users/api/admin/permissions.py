from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission

from users.models import SpecialistProfile

User = get_user_model()


class IsAdminUserRole(BasePermission):
    """
    Access to admin API:
    - superuser
    - employee
    - specialist with is_owner=True
    """

    def has_permission(self, request, view):
        user = request.user

        if user.is_superuser:
            return True

        if request.user == User.Role.EMPLOYEE:
            return True

        if user.role == User.Role.SPECIALIST:
            return SpecialistProfile.objects.filter(user=user, is_owner=True).exists()

        return False
