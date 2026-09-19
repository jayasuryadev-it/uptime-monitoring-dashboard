import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_trigger_health_check(client: AsyncClient):
    # Register & Login
    reg_resp = await client.post(
        "/api/v1/auth/register",
        json={"email": "checker_test@example.com", "password": "password123"}
    )
    token = reg_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create monitor targeting a known endpoint
    create_resp = await client.post(
        "/api/v1/monitors",
        headers=headers,
        json={"name": "HTTPBin Status 200", "url": "https://httpbin.org/status/200", "timeout": 5}
    )
    monitor_id = create_resp.json()["id"]

    # Trigger health check
    check_resp = await client.post(
        f"/api/v1/monitors/{monitor_id}/check",
        headers=headers
    )
    assert check_resp.status_code == 200
    check_data = check_resp.json()
    assert check_data["monitor_id"] == monitor_id
    assert check_data["status"] in ["UP", "DOWN"]
    assert "response_time" in check_data

    # Fetch health check history
    history_resp = await client.get(
        f"/api/v1/health-checks/monitors/{monitor_id}",
        headers=headers
    )
    assert history_resp.status_code == 200
    history = history_resp.json()
    assert len(history) >= 1
