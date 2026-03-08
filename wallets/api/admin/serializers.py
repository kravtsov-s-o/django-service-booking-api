from rest_framework import serializers

from wallets.models import ClientWalletTransaction


class AdminClientWalletTransactionSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source="wallet.client.user", read_only=True)
    type_display = serializers.CharField(source="get_type_display", read_only=True)

    class Meta:
        model = ClientWalletTransaction
        fields = (
            "id",
            "wallet",
            "client_name",
            "created_at",
            "amount",
            "type",
            "type_display",
            "balance_after",
            "service_record",
        )
        read_only_fields = (
            "id",
            "created_at",
            "balance_after",
            "type",
            "service_record",
        )

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Amount must be greater than 0. Only wallet top-up is allowed."
            )
        return value
