import pytest
from django.db import IntegrityError

from wallets.models import ClientWalletTransaction


def test_client_wallet_created(client_wallet):
    assert client_wallet is not None


def test_client_wallet_check(client_profile, client_wallet):
    assert client_wallet.client == client_profile
    assert client_wallet.balance == 0


def test_transaction_manual_topup(transaction_manual_topup):
    assert transaction_manual_topup is not None
    assert transaction_manual_topup.service_record is None
    assert transaction_manual_topup.type == ClientWalletTransaction.Type.MANUAL_TOPUP


def test_transaction_manual_topup_with_service(
    transaction_factory, client_wallet, create_service_record
):
    with pytest.raises(IntegrityError):
        transaction_factory(
            wallet=client_wallet,
            amount=100,
            type=ClientWalletTransaction.Type.MANUAL_TOPUP,
            service_record=create_service_record,
        )


def test_transaction_service_refund(transaction_service_refund):
    assert transaction_service_refund is not None
    assert transaction_service_refund.service_record is not None
    assert transaction_service_refund.type == ClientWalletTransaction.Type.REFUND


def test_transaction_refund_without_service(transaction_factory, client_wallet):
    with pytest.raises(IntegrityError):
        transaction_factory(
            wallet=client_wallet,
            amount=100,
            type=ClientWalletTransaction.Type.REFUND,
            service_record=None,
        )


def test_transaction_service_charge(transaction_service_charge):
    assert transaction_service_charge is not None
    assert transaction_service_charge.service_record is not None
    assert (
        transaction_service_charge.type == ClientWalletTransaction.Type.SERVICE_CHARGE
    )


def test_transaction_service_charge_without_service(transaction_factory, client_wallet):
    with pytest.raises(IntegrityError):
        transaction_factory(
            wallet=client_wallet,
            amount=100,
            type=ClientWalletTransaction.Type.SERVICE_CHARGE,
            service_record=None,
        )
