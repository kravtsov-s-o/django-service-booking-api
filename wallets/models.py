from django.db import models
from django.db.models import CheckConstraint, Q


# Create your models here.
class ClientWallet(models.Model):
    client = models.OneToOneField(
        "users.ClientProfile", on_delete=models.CASCADE, related_name="client_wallet"
    )
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.client} - {self.balance}"

    class Meta:
        verbose_name = "Client Wallet"
        verbose_name_plural = "Client Wallets"


MANUAL_TOPUP = 1
SERVICE_CHARGE = 2
REFUND = 3


class ClientWalletTransaction(models.Model):
    class Type(models.IntegerChoices):
        MANUAL_TOPUP = MANUAL_TOPUP
        SERVICE_CHARGE = SERVICE_CHARGE
        REFUND = REFUND

    wallet = models.ForeignKey(
        ClientWallet, on_delete=models.CASCADE, related_name="transactions"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.IntegerField(
        choices=Type.choices, default=Type.SERVICE_CHARGE, db_index=True
    )
    balance_after = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    service_record = models.ForeignKey(
        "appointments.ServiceRecord",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transactions",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.wallet} - {self.amount}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Wallet Transaction"
        verbose_name_plural = "Wallet Transactions"

        constraints = [
            CheckConstraint(
                condition=(
                    Q(type=MANUAL_TOPUP, service_record__isnull=True)
                    | Q(type__in=[SERVICE_CHARGE, REFUND], service_record__isnull=False)
                ),
                name="wallet_transaction_service_record_constraint",
            )
        ]
