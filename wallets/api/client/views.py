from django.views.generic import ListView
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
class ClientWalletView(APIView):
    permission_classes = [IsAuthenticated, IsClientUser]

    def get(self, request):
        wallet = request.user.client_profile.client_wallet
        serializer = ClientWalletSerializer(wallet)
        return Response(serializer.data)


class ClientWalletTransactionViewSet(GenericViewSet, ListModelMixin):
    permission_classes = [IsAuthenticated, IsClientUser]
    serializer_class = ClientWalletTransactionSerializer

    def get_queryset(self):
        wallet = self.request.user.client_profile.client_wallet
        return ClientWalletTransaction.objects.filter(wallet=wallet).select_related(
            "service_record"
        )
