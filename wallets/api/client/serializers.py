from rest_framework import serializers

from wallets.models import ClientWallet, ClientWalletTransaction


class ClientWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientWallet
        fields = ("balance",)


class ClientWalletTransactionSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source="get_type_display", read_only=True)

    class Meta:
        model = ClientWalletTransaction
        fields = (
            "created_at",
            "amount",
            "type",
            "type_display",
            "balance_after",
            "service_record",
        )
