import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_health_check_endpoint(api_client):
    response = await api_client.get("/health-check/")
    assert response.status_code == status.HTTP_200_OK, response.json()


@pytest.mark.asyncio
async def test_health_check_endpoint_raising_exception(api_client, mocker):
    mocker.patch(
        "poc_fastapi.app.health_check",
        side_effect=Exception("Database error"),
    )
    response = await api_client.get("/health-check/")
    assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE, response.json()
