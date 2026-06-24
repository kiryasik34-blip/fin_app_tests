import requests


def test_get_balance():
    login = "kik"
    url = "http://localhost:8000/api/v1/balance"

    response = requests.get(url=url, headers={"Authorization": f"Bearer {login}"})
    body = response.json()

    assert response.status_code == 200, f'должен быть 200 {response.content}'



