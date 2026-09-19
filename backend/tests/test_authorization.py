import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_user_isolation(client: AsyncClient):
    # Register User A
    user_a_resp = await client.post(
        "/api/v1/auth/register",
        json={"email": "usera@example.com", "password": "password123"}
    )
    headers_a = {"Authorization": f"Bearer {user_a_resp.json()['access_token']}"}

    # Register User B
    user_b_resp = await client.post(
        "/api/v1/auth/register",
        json={"email": "userb@example.com", "password": "password123"}
    )
    headers_b = {"Authorization": f"Bearer {user_b_resp.json()['access_token']}"}

    # User A creates a monitor
    mon_a = await client.post(
        "/api/v1/monitors",
        headers=headers_a,
        json={"name": "User A Monitor", "url": "https://example.com"}
    )
    monitor_a_id = mon_a.json()["id"]

    # User B attempts to access User A's monitor detail -> 404
    get_b = await client.get(f"/api/v1/monitors/{monitor_a_id}", headers=headers_b)
    assert get_b.status_code == 404

    # User B attempts to update User A's monitor -> 404
    put_b = await client.put(
        f"/api/v1/monitors/{monitor_a_id}",
        headers=headers_b,
        json={"name": "Hacked Name"}
    )
    assert put_b.status_code == 404

    # User B attempts to delete User A's monitor -> 404
    del_b = await client.delete(f"/api/v1/monitors/{monitor_a_id}", headers=headers_b)
    assert del_b.status_code == 404
