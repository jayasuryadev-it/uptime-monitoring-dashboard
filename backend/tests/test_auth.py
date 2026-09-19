import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    response = await client.post(
        "/api/v1/auth/register",
        json={"email": "testuser@example.com", "password": "securepassword123"}
    )
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["user"]["email"] == "testuser@example.com"


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient):
    await client.post(
        "/api/v1/auth/register",
        json={"email": "duplicate@example.com", "password": "password123"}
    )
    response = await client.post(
        "/api/v1/auth/register",
        json={"email": "duplicate@example.com", "password": "anotherpassword"}
    )
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


@pytest.mark.asyncio
async def test_login_user(client: AsyncClient):
    await client.post(
        "/api/v1/auth/register",
        json={"email": "loginuser@example.com", "password": "mypassword123"}
    )
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "loginuser@example.com", "password": "mypassword123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["email"] == "loginuser@example.com"


@pytest.mark.asyncio
async def test_login_invalid_password(client: AsyncClient):
    await client.post(
        "/api/v1/auth/register",
        json={"email": "wrongpwd@example.com", "password": "correctpassword"}
    )
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "wrongpwd@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401
