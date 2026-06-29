import time

import requests


def test_add_income():
    login = f"income_user_{int(time.time())}"

    requests.post(
        url="http://localhost:8000/api/v1/users",
        json={"login": login},
    )

    requests.post(
        url="http://localhost:8000/api/v1/wallets",
        headers={"Authorization": f"Bearer {login}"},
        json={"name": "income_wallet", "initial_balance": 1000, "currency": "rub"},
    )

    response = requests.post(
        url="http://localhost:8000/api/v1/operations/income",
        headers={"Authorization": f"Bearer {login}"},
        json={"wallet_name": "income_wallet", "amount": 500, "description": "salary"},
    )
    body = response.json()

    assert response.status_code == 200, f"must be 200 {response.text}"
    assert body["type"] == "income"
    assert float(body["amount"]) == 500.0
    assert body["currency"] == "rub"


def test_add_expense():
    login = f"expense_user_{int(time.time())}"

    requests.post(
        url="http://localhost:8000/api/v1/users",
        json={"login": login},
    )

    requests.post(
        url="http://localhost:8000/api/v1/wallets",
        headers={"Authorization": f"Bearer {login}"},
        json={"name": "expense_wallet", "initial_balance": 1000, "currency": "rub"},
    )

    response = requests.post(
        url="http://localhost:8000/api/v1/operations/expense",
        headers={"Authorization": f"Bearer {login}"},
        json={"wallet_name": "expense_wallet", "amount": 300, "description": "food"},
    )
    body = response.json()

    assert response.status_code == 200, f"must be 200 {response.text}"
    assert body["type"] == "expense"
    assert float(body["amount"]) == 300.0
    assert body["currency"] == "rub"


def test_get_operations():
    login = f"operations_user_{int(time.time())}"

    requests.post(
        url="http://localhost:8000/api/v1/users",
        json={"login": login},
    )

    requests.post(
        url="http://localhost:8000/api/v1/wallets",
        headers={"Authorization": f"Bearer {login}"},
        json={"name": "operations_wallet", "initial_balance": 1000, "currency": "rub"},
    )

    requests.post(
        url="http://localhost:8000/api/v1/operations/income",
        headers={"Authorization": f"Bearer {login}"},
        json={"wallet_name": "operations_wallet", "amount": 200, "description": "bonus"},
    )

    response = requests.get(
        url="http://localhost:8000/api/v1/operations",
        headers={"Authorization": f"Bearer {login}"},
    )
    body = response.json()

    assert response.status_code == 200, f"must be 200 {response.text}"
    assert len(body) > 0, "operations list must not be empty"

    operation = body[0]

    assert operation["type"] == "income"
    assert float(operation["amount"]) == 200.0
    assert operation["currency"] == "rub"


def test_create_transfer():
    login = f"transfer_user_{int(time.time())}"

    requests.post(
        url="http://localhost:8000/api/v1/users",
        json={"login": login},
    )

    first_wallet_response = requests.post(
        url="http://localhost:8000/api/v1/wallets",
        headers={"Authorization": f"Bearer {login}"},
        json={"name": "from_wallet", "initial_balance": 1000, "currency": "rub"},
    )
    second_wallet_response = requests.post(
        url="http://localhost:8000/api/v1/wallets",
        headers={"Authorization": f"Bearer {login}"},
        json={"name": "to_wallet", "initial_balance": 0, "currency": "rub"},
    )

    first_wallet = first_wallet_response.json()
    second_wallet = second_wallet_response.json()

    response = requests.post(
        url="http://localhost:8000/api/v1/operations/transfer",
        headers={"Authorization": f"Bearer {login}"},
        json={
            "from_wallet_id": first_wallet["id"],
            "to_wallet_id": second_wallet["id"],
            "amount": 250,
        },
    )
    body = response.json()

    assert response.status_code == 200, f"must be 200 {response.text}"
    assert body["type"] == "transfer"
    assert float(body["amount"]) == 250.0
    assert body["currency"] == "rub"
