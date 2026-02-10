from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

from users.models import SpecialistProfile, ClientProfile

User = get_user_model()


class AdminUserCreateSerializer(serializers.ModelSerializer):
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

        if user.role == User.Role.SPECIALIST:
            SpecialistProfile.objects.create(user=user)

        elif user.role == User.Role.CLIENT:
            ClientProfile.objects.create(user=user)

        return user


class AdminUserUpdateSerializer(serializers.ModelSerializer):
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
    new_password = serializers.CharField(required=True)
