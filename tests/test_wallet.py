import requests

import time

# def test_create_wallet():
#     login = f'user_{int(time.time())}'
#
#     requests.post(url="http://localhost:8000/api/v1/users", json={"login": login})
#
#     response = requests.post(url="http://localhost:8000/api/v1/wallets", headers={"Authorization": f"Bearer {login}"},
#                              json= {"name": "wallet1", "initial_balance":1000, "currency":"rub"})
#     body = response.json()
#
#     assert response.status_code == 200, f'must be dvesti{response.text}'
#     assert body['name'] == "wallet1"
#     assert float(body['balance']) == 1000.0
#     assert body['currency'] == "rub"

def test_get_wallets():
    login = f'user_{int(time.time())}'

    requests.post(url="http://localhost:8000/api/v1/users", json={"login": login})

    response = requests.post(url="http://localhost:8000/api/v1/wallets", headers={"Authorization": f"Bearer {login}"},
                             json={"name": "wallet_get", "initial_balance": 1488, "currency": "rub"})


    response = requests.get(url="http://localhost:8000/api/v1/wallets", headers={"Authorization": f"Bearer {login}"})
    body = response.json()

    assert response.status_code == 200, f'must be dvesti{response.text}'
    assert len(body) > 0, f'koshelkov > 0'

    wallet = body[0]

    assert wallet['name'] == 'wallet_get'
    assert float(wallet['balance']) == 1488.0
    assert wallet['currency'] == 'rub'


