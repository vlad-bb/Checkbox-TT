import pytest
from httpx import AsyncClient
from fastapi import status
from main import app


test_user = {
    "email": "testuser@example.com",
    "password": "TestPassword123",
    "username": "testuser",
    "business_name": "Test Business"
}

@pytest.mark.asyncio
async def test_signup():
    """
    Test the signup process with a new user.
    - Should return status 201 and user details on success.
    - Should return status 409 if the user already exists.
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/auth/signup", json=test_user)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["email"] == test_user["email"]

        response = await ac.post("/auth/signup", json=test_user)
        assert response.status_code == status.HTTP_409_CONFLICT
        assert response.json()["detail"] == "Account already exists!"

@pytest.mark.asyncio
async def test_login():
    """
    Test the login process with the existing user.
    - Should return 200 with access and refresh tokens.
    - Should return 401 for invalid credentials.
    """
    login_data = {"email": test_user["email"], "password": test_user["password"]}

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/auth/login", json=login_data)
        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.json()
        assert "refresh_token" in response.json()

        response = await ac.post("/auth/login", json={"email": test_user["email"], "password": "wrongpassword"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()["detail"] == "Incorrect registration information!"

@pytest.mark.asyncio
async def test_refresh_token():
    """
    Test refreshing the access token with a valid refresh token.
    - Should return new access and refresh tokens on success.
    - Should return 401 for an invalid refresh token.
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        login_response = await ac.post("/auth/login", json={"email": test_user["email"], "password": test_user["password"]})
        refresh_token = login_response.json()["refresh_token"]

        headers = {"Authorization": f"Bearer {refresh_token}"}
        response = await ac.get("/auth/refresh_token", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.json()
        assert "refresh_token" in response.json()

        headers = {"Authorization": "Bearer invalidtoken"}
        response = await ac.get("/auth/refresh_token", headers=headers)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()["detail"] == "Could not validate credentials!"
