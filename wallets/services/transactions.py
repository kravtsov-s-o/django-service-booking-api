from decimal import Decimal

from django.db import transaction

from appointments.models import ServiceRecord
from wallets.models import ClientWallet, ClientWalletTransaction


def create_wallet_transaction(
    *,
    wallet_id: int,
    amount: Decimal,
    transaction_type: int,
    service_record: ServiceRecord | None = None,
) -> ClientWalletTransaction:
    """
    Create a wallet transaction and update the client's wallet balance.

    The function records the transaction and recalculates the wallet balance.
    Used for:
    - manual top-up
    - service charge
    - refund
    """

    with transaction.atomic():
        locked_wallet = ClientWallet.objects.select_for_update().get(pk=wallet_id)

        new_balance = locked_wallet.balance + amount

        client_transaction = ClientWalletTransaction.objects.create(
            wallet=locked_wallet,
            amount=amount,
            type=transaction_type,
            balance_after=new_balance,
            service_record=service_record,
        )

        locked_wallet.balance = new_balance
        locked_wallet.save(update_fields=["balance"])

        return client_transaction
