import pytest
from httpx import AsyncClient


async def get_auth_headers(client: AsyncClient, email: str = "monitor_test@example.com") -> dict:
    reg_resp = await client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "password123"}
    )
    token = reg_resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_create_and_list_monitors(client: AsyncClient):
    headers = await get_auth_headers(client, "user1@example.com")

    # Create monitor
    create_resp = await client.post(
        "/api/v1/monitors",
        headers=headers,
        json={"name": "Google", "url": "https://google.com", "interval": 60, "timeout": 10}
    )
    assert create_resp.status_code == 201
    monitor = create_resp.json()
    assert monitor["name"] == "Google"
    assert monitor["url"] == "https://google.com"

    # List monitors
    list_resp = await client.get("/api/v1/monitors", headers=headers)
    assert list_resp.status_code == 200
    monitors = list_resp.json()
    assert len(monitors) == 1
    assert monitors[0]["id"] == monitor["id"]


@pytest.mark.asyncio
async def test_update_and_delete_monitor(client: AsyncClient):
    headers = await get_auth_headers(client, "user2@example.com")

    create_resp = await client.post(
        "/api/v1/monitors",
        headers=headers,
        json={"name": "Original Name", "url": "https://example.com"}
    )
    monitor_id = create_resp.json()["id"]

    # Update monitor
    update_resp = await client.put(
        f"/api/v1/monitors/{monitor_id}",
        headers=headers,
        json={"name": "Updated Name", "interval": 120}
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["name"] == "Updated Name"
    assert update_resp.json()["interval"] == 120

    # Delete monitor
    del_resp = await client.delete(f"/api/v1/monitors/{monitor_id}", headers=headers)
    assert del_resp.status_code == 204

    # Verify deleted
    list_resp = await client.get("/api/v1/monitors", headers=headers)
    assert len(list_resp.json()) == 0
