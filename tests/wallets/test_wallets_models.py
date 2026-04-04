def test_client_wallet_created(client_wallet):
    assert client_wallet is not None


def test_client_wallet_check(client_profile, client_wallet):
    assert client_wallet.client == client_profile
    assert client_wallet.balance == 0
