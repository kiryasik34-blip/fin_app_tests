import requests


def test_get_balance():
    login = "kik"
    url = "http://localhost:8000/api/v1/balance"

    response = requests.get(url=url, headers={"Authorization": f"Bearer {login}"})
    body = response.json()

    assert response.status_code == 200, f'должен быть 200 {response.content}'
    assert len(body) == 0, f"негативный тест. ,balance не должен быть пустым. {response.content}"

def test_get_wallets():
    login = "kik"
    url = "http://localhost:8000/api/v1/wallets"

    response = requests.get(url, headers={"Authorization": f"Bearer {login}"})
    body = response.json()

    wallet = body[0]
    assert response.status_code == 200
    assert len(body) > 0
    assert float(wallet["balance"]) == 1000.0



