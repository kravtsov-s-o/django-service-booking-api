from rest_framework import serializers

from services.models import Service, SpecialistService


class AdminServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = (
            "id",
            "title",
            "description",
            "base_price",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")


class AdminSpecialistServiceSerializer(serializers.ModelSerializer):
    specialist_name = serializers.CharField(
        source="specialist.user.full_name", read_only=True
    )
    service_title = serializers.CharField(source="service.title", read_only=True)

    payout_type_display = serializers.CharField(
        source="get_payout_type_display", read_only=True
    )

    class Meta:
        model = SpecialistService
        fields = (
            "id",
            "specialist",
            "specialist_name",
            "service",
            "service_title",
            "payout_type",
            "payout_type_display",
            "payout_value",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")

    def validate(self, attrs):
        service = attrs["service"]
        payout_type = attrs["payout_type"]
        payout_value = attrs["payout_value"]

        if service and not service.is_active:
            raise serializers.ValidationError(
                {"service": "Cannot assign archived service."}
            )

        if payout_type == SpecialistService.Type.FULL and payout_value:
            raise serializers.ValidationError(
                {"payout_value": "Should be empty when payout type is FULL."}
            )

        if payout_type == SpecialistService.Type.FIXED and not payout_value:
            raise serializers.ValidationError(
                {"payout_value": "Required when payout type is FIXED."}
            )

        return attrs
