from core.api.routers import build_router
from wallets.api.admin.views import AdminClientWalletTransactionViewSet

urlpatterns = build_router(
    ("transactions", AdminClientWalletTransactionViewSet, "admin-transactions")
)
