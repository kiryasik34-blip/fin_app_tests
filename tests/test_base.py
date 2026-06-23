import requests


def auth_headers(login: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {login}"}


def test_create_user():
    url = "http://localhost:8000/api/v1/users"
    user_name = "test3"
    data = {"login": user_name}

    response = requests.post(url=url, json=data)
    body = response.json()

    assert response.status_code == 200, f"Должен быть верный статус код. {response.content}"
    assert body.get("login") == user_name, f"Имя созданного юзера должно быть. {response.content}"


def test_get_user():
    url = "http://localhost:8000/api/v1/users/me"
    user_name = "test"

    response = requests.get(url=url, headers=auth_headers(user_name))
    body = response.json()

    assert response.status_code == 200, f"Должен быть верный статус код. {response.content}"
    assert body.get("login") == user_name, f"Имя созданного юзера должно быть. {response.content}"
