from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.api.fields import UserRoleField

User = get_user_model()


class MeSerializer(serializers.ModelSerializer):
    """
    Serializer for representing and updating the current user.
    """

    role = UserRoleField(read_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "username", "first_name", "last_name", "role")
        read_only_fields = ("id", "role")


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)
