from rest_framework.permissions import BasePermission

from users.models import ClientProfile, SpecialistProfile


class IsClientUser(BasePermission):
    """
    Allow access only to users that have a ClientProfile
    """

    def has_permission(self, request, view):
        return ClientProfile.objects.filter(user=request.user).exists()


class IsSpecialistUser(BasePermission):
    """
    Allow access only to users that have a SpecialistProfile
    """

    def has_permission(self, request, view):
        return SpecialistProfile.objects.filter(user=request.user).exists()
