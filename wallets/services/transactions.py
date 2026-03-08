from wallets.models import ClientWalletTransaction


def create_wallet_transaction(wallet, amount, type, service_record=None):
    new_balance = wallet.balance + amount

    transaction = ClientWalletTransaction.objects.create(
        wallet=wallet,
        amount=amount,
        type=type,
        balance_after=new_balance,
        service_record=service_record,
    )

    wallet.balance = new_balance
    wallet.save(update_fields=["balance"])

    return transaction
