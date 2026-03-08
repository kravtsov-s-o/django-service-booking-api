from django.db import transaction
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from users.api.admin.permissions import IsAdminUserRole
from wallets.api.admin.serializers import AdminClientWalletTransactionSerializer
from wallets.models import ClientWalletTransaction
from wallets.services.transactions import create_wallet_transaction


class AdminClientWalletTransactionViewSet(
    GenericViewSet, ListModelMixin, CreateModelMixin
):
    permission_classes = [IsAuthenticated, IsAdminUserRole]
    serializer_class = AdminClientWalletTransactionSerializer
    queryset = ClientWalletTransaction.objects.all().select_related(
        "wallet",
        "wallet__client",
        "wallet__client__user",
        "service_record",
    )

    def perform_create(self, serializer):
        # serializer.save(type=ClientWalletTransaction.Type.MANUAL_TOPUP)
        wallet = serializer.validated_data["wallet"]
        amount = serializer.validated_data["amount"]
        transaction_type = ClientWalletTransaction.Type.MANUAL_TOPUP

        with transaction.atomic():
            create_wallet_transaction(
                wallet=wallet,
                amount=amount,
                type=transaction_type
            )
