import pytest
from httpx import AsyncClient
from fastapi import status


@pytest.mark.asyncio
async def test_show_check_html_success(client: AsyncClient, token: str, check_object: dict):
    """
    Test retrieving an HTML view of a check with a valid check ID.
    """
    headers = {"Authorization": f"Bearer {token}"}

    response = await client.post("/api/check/", json=check_object, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED, response.text
    created_check = response.json()
    check_id = created_check["id"]

    response = await client.get(f"/{check_id}/html", headers=headers)
    assert response.status_code == status.HTTP_200_OK, response.text

    assert "<!DOCTYPE html>" in response.text
    assert str(check_id) in response.text


@pytest.mark.asyncio
async def test_show_check_html_not_found(client: AsyncClient, token: str):
    """
    Test retrieving an HTML view with an invalid check ID.
    """
    headers = {"Authorization": f"Bearer {token}"}
    invalid_check_id = 99999

    response = await client.get(f"/check/{invalid_check_id}/html", headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text
    data = response.json()
    assert data["detail"] == 'Not Found'


@pytest.mark.asyncio
async def test_show_check_txt_success(client: AsyncClient, token: str, check_object: dict):
    """
    Test retrieving a TXT view of a check with a valid check ID.
    """
    headers = {"Authorization": f"Bearer {token}"}

    response = await client.post("/api/check/", json=check_object, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED, response.text
    created_check = response.json()
    check_id = created_check["id"]

    response = await client.get(f"/{check_id}/txt?line_width=32", headers=headers)
    assert response.status_code == status.HTTP_200_OK, response.text

    assert str(check_id) in response.text


@pytest.mark.asyncio
async def test_show_check_txt_not_found(client: AsyncClient, token: str):
    """
    Test retrieving a TXT view with an invalid check ID.
    """
    headers = {"Authorization": f"Bearer {token}"}
    invalid_check_id = 99999

    response = await client.get(f"/{invalid_check_id}/txt", headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text
    data = response.json()
    assert data["detail"] == f"Check ID: {invalid_check_id} not found"


@pytest.mark.asyncio
async def test_show_check_qr_success(client: AsyncClient, token: str, check_object: dict):
    """
    Test retrieving a QR code view of a check with a valid check ID.
    """
    headers = {"Authorization": f"Bearer {token}"}

    response = await client.post("/api/check/", json=check_object, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED, response.text
    created_check = response.json()
    check_id = created_check["id"]

    response = await client.get(f"/{check_id}/qr-code?mode=html", headers=headers)
    assert response.status_code == status.HTTP_200_OK, response.text

    assert response.headers["content-type"] == "image/png"


@pytest.mark.asyncio
async def test_show_check_qr_not_found(client: AsyncClient, token: str):
    """
    Test retrieving a QR code with an invalid check ID.
    """
    headers = {"Authorization": f"Bearer {token}"}
    invalid_check_id = 99999

    response = await client.get(f"/{invalid_check_id}/qr-code?mode=html", headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text
    data = response.json()
    assert data["detail"] == f"Check ID: {invalid_check_id} not found"
