import pytest

from fastapi import status
from src.conf import messages


@pytest.mark.asyncio
async def test_create_user(client, user):
    """
    Test that a user can successfully sign up.
    """
    response = await client.post(
        "/api/auth/signup",
        json=user,
    )
    assert response.status_code == status.HTTP_201_CREATED, response.text
    data = response.json()
    assert data["username"] == user.get("username")
    assert data["email"] == user.get("email")
    assert "password" not in data
    assert "business_name" in data


@pytest.mark.asyncio
async def test_repeat_create_user(client, user):
    """
    Test that attempting to sign up with an existing email returns a conflict error.
    """
    response = await client.post(
        "/api/auth/signup",
        json=user,
    )
    assert response.status_code == status.HTTP_409_CONFLICT, response.text
    data = response.json()
    assert data["detail"] == messages.ACCOUNT_EXIST


@pytest.mark.asyncio
async def test_login_user(client, user):
    """
    Test that a user can successfully log in.
    """
    response = await client.post(
        "/api/auth/login",
        json={"email": user.get("email"), "password": user.get("password")},
    )
    assert response.status_code == status.HTTP_200_OK, response.text
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert "token_type" in data


@pytest.mark.asyncio
async def test_login_wrong_password(client, user):
    """
    Test that logging in with an incorrect password returns an unauthorized error.
    """
    response = await client.post(
        "/api/auth/login",
        json={"email": user.get("email"), "password": "wrong_password"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.text
    data = response.json()
    assert data["detail"] == messages.WRONG_PASSWORD


@pytest.mark.asyncio
async def test_login_not_found_email(client, user):
    """
    Test that logging in with a non-existent email returns an unauthorized error.
    """
    response = await client.post(
        "/api/auth/login",
        json={"email": "example@email.com", "password": user.get("password")},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.text
    data = response.json()
    assert data["detail"] == messages.NOT_CONTACT


@pytest.mark.asyncio
async def test_validation_error_login(client, user):
    """
    Test that sending an incomplete login request returns a validation error.
    """
    response = await client.post("api/auth/login",
                                 json={"password": user.get("password")})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text
    data = response.json()
    assert "detail" in data


@pytest.mark.asyncio
async def test_refresh_token_successful(client, user):
    """
    Test that a valid refresh token can successfully generate new access and refresh tokens.
    """
    await client.post("/api/auth/signup", json=user)
    login_response = await client.post(
        "/api/auth/login",
        json={"email": user.get("email"), "password": user.get("password")},
    )
    assert login_response.status_code == status.HTTP_200_OK
    tokens = login_response.json()
    refresh_token = tokens["refresh_token"]
    refresh_response = await client.get(
        "/api/auth/refresh_token",
        headers={"Authorization": f"Bearer {refresh_token}"}
    )
    assert refresh_response.status_code == status.HTTP_200_OK, refresh_response.text
    data = refresh_response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "Bearer"


@pytest.mark.asyncio
async def test_refresh_token_unsuccessful(client, user):
    """
    Test that using an invalid refresh token returns an unauthorized error.
    """
    invalid_refresh_token = "invalid_refresh_token"
    refresh_response = await client.get(
        "/api/auth/refresh_token",
        headers={"Authorization": f"Bearer {invalid_refresh_token}"}
    )
    assert refresh_response.status_code == status.HTTP_401_UNAUTHORIZED
    assert refresh_response.json()["detail"] == messages.CREDENTIALS_INVALID

