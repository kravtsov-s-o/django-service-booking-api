from django.db import transaction
from drf_spectacular.utils import extend_schema
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from users.api.admin.permissions import IsAdminUserRole
from wallets.api.admin.serializers import AdminClientWalletTransactionSerializer
from wallets.models import ClientWalletTransaction
from wallets.services.transactions import create_wallet_transaction


@extend_schema(tags=["Admin: Wallet"], summary="Admin wallet transactions management")
class AdminClientWalletTransactionViewSet(
    GenericViewSet, ListModelMixin, CreateModelMixin
):
    """
    Admin wallet transaction management.

    Endpoints:
    - GET /admin/wallet-transactions/  — list all wallet transactions
    - POST /admin/wallet-transactions/ — manually top up a client wallet

    Permissions:
    Admin users only.
    """

    permission_classes = [IsAuthenticated, IsAdminUserRole]
    serializer_class = AdminClientWalletTransactionSerializer
    queryset = ClientWalletTransaction.objects.all().select_related(
        "wallet",
        "wallet__client",
        "wallet__client__user",
        "service_record",
    )

    def perform_create(self, serializer):
        wallet = serializer.validated_data["wallet"]
        amount = serializer.validated_data["amount"]
        transaction_type = ClientWalletTransaction.Type.MANUAL_TOPUP

        with transaction.atomic():
            create_wallet_transaction(
                wallet=wallet, amount=amount, transaction_type=transaction_type
            )
