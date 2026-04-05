from decimal import Decimal

import pytest

from wallets.models import ClientWalletTransaction
from wallets.services.transactions import create_wallet_transaction


@pytest.mark.parametrize(
    ("amount", "transaction_type", "use_service_record"),
    [
        (Decimal("100.00"), ClientWalletTransaction.Type.MANUAL_TOPUP, False),
        (Decimal("-100.00"), ClientWalletTransaction.Type.SERVICE_CHARGE, True),
        (Decimal("100.00"), ClientWalletTransaction.Type.REFUND, True),
    ],
)
def test_create_wallet_transaction_updates_balance(
    client_wallet,
    create_service_record,
    amount,
    transaction_type,
    use_service_record,
):
    old_balance = client_wallet.balance
    service_record = create_service_record if use_service_record else None

    wallet_transaction = create_wallet_transaction(
        wallet_id=client_wallet.pk,
        amount=amount,
        transaction_type=transaction_type,
        service_record=service_record,
    )

    assert wallet_transaction is not None
    assert wallet_transaction.wallet_id == client_wallet.pk
    assert wallet_transaction.amount == amount
    assert wallet_transaction.type == transaction_type
    assert wallet_transaction.service_record == service_record
    assert wallet_transaction.balance_after == old_balance + amount

    client_wallet.refresh_from_db()
    assert client_wallet.balance == old_balance + amount
    assert client_wallet.balance == wallet_transaction.balance_after
