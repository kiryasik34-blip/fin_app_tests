import time

import requests


def auth_headers(login: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {login}"}


def test_create_user():
    url = "http://localhost:8000/api/v1/users"
    user_name = f"test3_{time.time_ns()}"
    data = {"login": user_name}

    response = requests.post(url=url, json=data)
    body = response.json()

    assert response.status_code == 200, f"Должен быть верный статус код. {response.content}"
    assert body.get("login") == user_name, f"Имя созданного юзера должно быть. {response.content}"
    assert "id" in body, f"В ответе должно быть поле id. {response.content}"


def test_get_user():
    create_user_url = "http://localhost:8000/api/v1/users"
    get_user_url = "http://localhost:8000/api/v1/users/me"
    user_name = f"test_{time.time_ns()}"

    requests.post(url=create_user_url, json={"login": user_name})

    response = requests.get(url=get_user_url, headers=auth_headers(user_name))
    body = response.json()

    assert response.status_code == 200, f"Должен быть верный статус код. {response.content}"
    assert body.get("login") == user_name, f"Имя созданного юзера должно быть. {response.content}"


def test_get_user_not_found_returns_401():
    url = "http://localhost:8000/api/v1/users/me"
    user_name = f"missing_user_{time.time_ns()}"

    response = requests.get(url=url, headers=auth_headers(user_name))

    assert response.status_code == 401, f"Должен быть статус код 401. {response.content}"


def test_create_two_users_have_different_ids():
    url = "http://localhost:8000/api/v1/users"
    first_user_name = f"first_user_{time.time_ns()}"
    second_user_name = f"second_user_{time.time_ns()}"

    first_response = requests.post(url=url, json={"login": first_user_name})
    second_response = requests.post(url=url, json={"login": second_user_name})

    first_body = first_response.json()
    second_body = second_response.json()

    assert first_response.status_code == 200, f"Должен быть верный статус код. {first_response.content}"
    assert second_response.status_code == 200, f"Должен быть верный статус код. {second_response.content}"
    assert first_body["id"] != second_body["id"], "У двух разных пользователей должны быть разные id"
