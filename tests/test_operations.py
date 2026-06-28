import requests

import time

def test_add_income():
    login = f'income_user_{int(time.time())}'

    requests.post(url="http://localhost:8000/api/v1/users", json={"login": login})

    requests.post(url="http://localhost:8000/api/v1/wallets", headers={"Authorization": f"Bearer {login}"},
                  json= {"name":"walentin", "initial_balance":"14881337", "currency":"rub"})
    response = requests.post(url="http://localhost:8000/api/v1/operations/income",
                             headers={"Authorization": f"Bearer {login}"},
                             json={"wallet_name":"walentin", "amount":"228", "description": "salary"})
    body = response.json()

    assert response.status_code == 200, {response.content}
    assert body['type'] == 'income'
    assert float(body['amount']) == 228
    assert len(body) > 0


