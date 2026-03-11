from decimal import Decimal

from appointments.models import ServiceRecord
from wallets.models import ClientWallet, ClientWalletTransaction


def create_wallet_transaction(
        *,
        wallet: ClientWallet,
        amount: Decimal,
        transaction_type: int,
        service_record: ServiceRecord | None = None
) -> ClientWalletTransaction:
    """
    Create a wallet transaction and update the client's wallet balance.

    The function records the transaction and recalculates the wallet balance.
    Used for:
    - manual top-up
    - service charge
    - refund
    """
    new_balance = wallet.balance + amount

    transaction = ClientWalletTransaction.objects.create(
        wallet=wallet,
        amount=amount,
        type=transaction_type,
        balance_after=new_balance,
        service_record=service_record,
    )

    wallet.balance = new_balance
    wallet.save(update_fields=["balance"])

    return transaction
