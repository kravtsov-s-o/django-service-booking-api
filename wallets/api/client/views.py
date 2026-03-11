from drf_spectacular.utils import extend_schema
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from users.api.permissions import IsClientUser
from wallets.api.client.serializers import (
    ClientWalletSerializer,
    ClientWalletTransactionSerializer,
)
from wallets.models import ClientWalletTransaction


# Create your views here.
@extend_schema(tags=["Profile: Client Wallet"],
    summary="Retrieve client wallet balance")
class ClientWalletView(APIView):
    """
    Retrieve the wallet balance for the authenticated client.

    Returns the current wallet balance associated with the client profile.

    Permissions:
    Client users only.
    """
    permission_classes = [IsAuthenticated, IsClientUser]

    def get(self, request):
        wallet = request.user.client_profile.client_wallet
        serializer = ClientWalletSerializer(wallet)
        return Response(serializer.data)


@extend_schema(tags=["Profile: Client Wallet"],
    summary="Retrieve for client wallet transactions")
class ClientWalletTransactionViewSet(GenericViewSet, ListModelMixin):
    """
    List wallet transactions for the authenticated client.

    Returns the history of wallet operations including:
    - manual top-ups
    - service charges
    - refunds

    Permissions:
    Client users only.
    """
    permission_classes = [IsAuthenticated, IsClientUser]
    serializer_class = ClientWalletTransactionSerializer

    def get_queryset(self):
        wallet = self.request.user.client_profile.client_wallet
        return ClientWalletTransaction.objects.filter(wallet=wallet).select_related(
            "service_record"
        )
