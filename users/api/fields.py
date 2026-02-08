from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserRoleField(serializers.Field):
    """
    Represent User.role as a readable string in responses
    and accept integer values in requests.
    """

    def to_representation(self, value):
        # value is integer from DB
        return User.Role(value).name.lower()

    def to_internal_value(self, data):
        # allow swending integer role
        try:
            return int(data)
        except (TypeError, ValueError):
            raise serializers.ValidationError("Role must be an integer")
