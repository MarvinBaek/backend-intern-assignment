import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user():
    def _create_user(username, password, nickname="기본닉네임"):
        return User.objects.create_user(username=username, password=password, nickname=nickname)
    return _create_user


@pytest.mark.django_db
def test_signup_success(api_client):
    data = {
        "username": "newuser",
        "password": "securepassword123",
        "nickname": "Newbie"
    }
    response = api_client.post("/signup", data)
    assert response.status_code == 201
    assert response.data["username"] == "newuser"
    assert response.data["nickname"] == "Newbie"


@pytest.mark.django_db
def test_signup_duplicate(api_client, create_user):
    create_user("existinguser", "pass1234", "닉네임")
    data = {
        "username": "existinguser",
        "password": "pass1234",
        "nickname": "다른닉네임"
    }
    response = api_client.post("/signup", data)
    assert response.status_code == 400
    assert "error" in response.data
    assert response.data["error"]["code"] == "USER_ALREADY_EXISTS"

@pytest.mark.django_db
def test_login_success(api_client, create_user):
    create_user("testuser", "testpass123", "닉네임")
    data = {
        "username": "testuser",
        "password": "testpass123"
    }
    response = api_client.post("/login", data)
    assert response.status_code == 200
    assert "token" in response.data

@pytest.mark.django_db
def test_login_fail_wrong_password(api_client, create_user):
    create_user("testuser", "correctpass", "닉네임")
    data = {
        "username": "testuser",
        "password": "wrongpass"
    }
    response = api_client.post("/login", data)
    assert response.status_code == 401
    assert "error" in response.data
    assert response.data["error"]["code"] == "INVALID_CREDENTIALS"
