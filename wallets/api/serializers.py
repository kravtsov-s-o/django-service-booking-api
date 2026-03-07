from rest_framework import serializers

from wallets.models import ClientWallet


class ClientWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientWallet
        fields = ("balance",)
