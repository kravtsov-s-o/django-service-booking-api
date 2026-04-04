from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

User = get_user_model()


class AdminUserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating users through the admin API.

    Used by administrators to create new users in the system.

    Behaviour:
    - Password is write-only and is hashed before saving.
    - Depending on the selected role, the corresponding profile is created:
        * SpecialistProfile for specialists
        * ClientProfile for clients
    """

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "role",
            "is_active",
            "password",
        )
        read_only_fields = ("id",)

    @transaction.atomic
    def create(self, validated_data):
        password = validated_data.pop("password")

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user


class AdminUserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user information via the admin API.

    Allows updating basic user fields such as:
    email, username, first name, last name, and active status.

    Restrictions:
    - The user role cannot be changed once the user is created.
    """

    role = serializers.CharField(source="get_role_display", read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "role",
            "is_active",
        )
        read_only_fields = ("id", "role")

    def validate(self, attrs):
        if "role" in attrs:
            raise serializers.ValidationError(
                {"role": "Changing user role is not allowed."}
            )
        return attrs


class AdminSetPasswordSerializer(serializers.Serializer):
    """
    Serializer used by administrators to reset a user's password.
    """

    new_password = serializers.CharField(required=True, write_only=True)
