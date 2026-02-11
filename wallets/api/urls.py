from django.urls import path
from wallets.api.views import ClientWalletView

urlpatterns = [
    path("wallet/", ClientWalletView.as_view(), name="my-wallet"),
]
