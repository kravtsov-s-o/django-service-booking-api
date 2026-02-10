from rest_framework.permissions import BasePermission

from users.models import ClientProfile


class IsClientUser(BasePermission):
    """
    Allow access only to users that have a ClientProfile
    """

    def has_permission(self, request, view):
        return ClientProfile.objects.filter(user=request.user).exists()
