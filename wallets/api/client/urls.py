from django.urls import path

from core.api.routers import build_router
from wallets.api.client.views import ClientWalletView, ClientWalletTransactionViewSet

transaction_urls = build_router(
    ("transactions", ClientWalletTransactionViewSet, "client-transactions")
)

urlpatterns = [
    path("wallet/", ClientWalletView.as_view(), name="my-wallet"),
] + transaction_urls
