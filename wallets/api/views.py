from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.api.permissions import IsClientUser
from wallets.api.serializers import ClientWalletSerializer


# Create your views here.
class ClientWalletView(APIView):
    permission_classes = [IsAuthenticated, IsClientUser]

    def get(self, request):
        wallet = request.user.client_profile.client_wallet
        serializer = ClientWalletSerializer(wallet)
        return Response(serializer.data)
