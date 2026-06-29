import time

import requests


def test_create_wallet():
    login = f"create_wallet_user_{int(time.time())}"

    requests.post(
        url="http://localhost:8000/api/v1/users",
        json={"login": login},
    )

    response = requests.post(
        url="http://localhost:8000/api/v1/wallets",
        headers={"Authorization": f"Bearer {login}"},
        json={"name": "wallet1", "initial_balance": 1000, "currency": "rub"},
    )
    body = response.json()

    assert response.status_code == 200, f"must be 200 {response.text}"
    assert body["name"] == "wallet1"
    assert float(body["balance"]) == 1000.0
    assert body["currency"] == "rub"


def test_get_wallets():
    login = f"get_wallets_user_{int(time.time())}"

    requests.post(
        url="http://localhost:8000/api/v1/users",
        json={"login": login},
    )

    requests.post(
        url="http://localhost:8000/api/v1/wallets",
        headers={"Authorization": f"Bearer {login}"},
        json={"name": "wallet_get", "initial_balance": 1488, "currency": "rub"},
    )

    response = requests.get(
        url="http://localhost:8000/api/v1/wallets",
        headers={"Authorization": f"Bearer {login}"},
    )
    body = response.json()

    assert response.status_code == 200, f"must be 200 {response.text}"
    assert len(body) > 0, "wallets list must not be empty"

    wallet = body[0]

    assert wallet["name"] == "wallet_get"
    assert float(wallet["balance"]) == 1488.0
    assert wallet["currency"] == "rub"


def test_get_balance():
    login = f"get_balance_user_{int(time.time())}"

    requests.post(
        url="http://localhost:8000/api/v1/users",
        json={"login": login},
    )

    requests.post(
        url="http://localhost:8000/api/v1/wallets",
        headers={"Authorization": f"Bearer {login}"},
        json={"name": "wallet_balance", "initial_balance": 1000, "currency": "rub"},
    )

    response = requests.get(
        url="http://localhost:8000/api/v1/balance",
        headers={"Authorization": f"Bearer {login}"},
    )
    body = response.json()

    assert response.status_code == 200, f"must be 200 {response.text}"
    assert float(body["total_balance"]) == 1000.0
