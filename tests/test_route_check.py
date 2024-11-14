import pytest
from httpx import AsyncClient
from fastapi import status
from datetime import datetime, timedelta
from src.conf import messages


@pytest.mark.asyncio
async def test_create_check_success(client: AsyncClient, check_object: dict, token: str):
    """
        Test that a user can successfully create a new check.
    """
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.post("/api/check/", json=check_object, headers=headers)

    assert response.status_code == status.HTTP_201_CREATED, response.text
    data = response.json()
    assert "id" in data
    assert data["payment"]["type"] == check_object["payment"]["type"]
    assert float(data["payment"]["amount"]) == float(check_object["payment"]["amount"])
    assert data["total"] == str(sum(
        product["price"] * product["quantity"] for product in check_object["products"]
    ))
    assert data["rest"] == str((
            check_object["payment"]["amount"]
            - sum(product["price"] * product["quantity"] for product in check_object["products"])
    ))
    assert len(data["products"]) == len(check_object["products"])
    for i, product in enumerate(data["products"]):
        assert product["name"] == check_object["products"][i]["name"]
        assert float(product["price"]) == float(check_object["products"][i]["price"])
        assert product["quantity"] == check_object["products"][i]["quantity"]
        assert float(product["total"]) == float(
            check_object["products"][i]["price"] * check_object["products"][i]["quantity"]
        )
    assert "links" in data
    assert "link_html" in data["links"]
    assert "link_txt" in data["links"]
    assert "link_qr" in data["links"]


@pytest.mark.asyncio
async def test_create_check_insufficient_payment(client: AsyncClient, token: str):
    """
    Test that a check cannot be created if the payment amount is insufficient.
    """
    headers = {"Authorization": f"Bearer {token}"}
    check_object = {
        "payment": {
            "amount": 100.0,
            "type": "cash"
        },
        "products": [
            {
                "name": "Mavic 3T",
                "price": 298870.5,
                "quantity": 3
            }
        ]
    }

    response = await client.post("/api/check/", json=check_object, headers=headers)

    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.text
    data = response.json()
    assert data["detail"] == messages.PAYMENT_AMOUNT_INVALID


@pytest.mark.asyncio
async def test_create_check_missing_field(client: AsyncClient, token: str):
    """
    Test that creating a check fails if a required field is missing.
    """
    headers = {"Authorization": f"Bearer {token}"}
    check_object = {
        "payment": {
            "amount": 300.0,
            "type": "cash"
        }
    }
    response = await client.post("/api/check/", json=check_object, headers=headers)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text
    data = response.json()
    assert "detail" in data
    assert any(error["loc"] == ["body", "products"] for error in data["detail"])


@pytest.mark.asyncio
async def test_create_check_invalid_token(client: AsyncClient, check_object: dict):
    """
    Test that creating a check fails with an invalid token.
    """
    headers = {"Authorization": "Bearer invalid_token"}
    response = await client.post("/api/check/", json=check_object, headers=headers)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.text
    data = response.json()
    assert data["detail"] == messages.CREDENTIALS_INVALID


@pytest.mark.asyncio
async def test_create_check_unauthenticated(client: AsyncClient, check_object: dict):
    """
    Test that creating a check fails when no token is provided.
    """
    response = await client.post("/api/check/", json=check_object)

    assert response.status_code == status.HTTP_403_FORBIDDEN, response.text
    data = response.json()
    assert data["detail"] == messages.NOT_AUTH


@pytest.mark.asyncio
async def test_read_check_success(client: AsyncClient, token: str, check_object: dict):
    """
    Test that a check can be successfully retrieved by ID.
    """
    headers = {"Authorization": f"Bearer {token}"}

    create_response = await client.post("/api/check/", json=check_object, headers=headers)
    assert create_response.status_code == status.HTTP_201_CREATED, create_response.text

    created_check = create_response.json()
    check_id = created_check["id"]

    retrieve_response = await client.get(f"/api/check/find/{check_id}", headers=headers)
    assert retrieve_response.status_code == status.HTTP_200_OK, retrieve_response.text

    data = retrieve_response.json()
    assert data["id"] == check_id
    assert data["payment"]["type"] == check_object["payment"]["type"]
    assert float(data["payment"]["amount"]) == float(check_object["payment"]["amount"])
    assert float(data["total"]) == sum(product["price"] * product["quantity"] for product in check_object["products"])
    assert float(data["rest"]) == check_object["payment"]["amount"] - sum(
        product["price"] * product["quantity"] for product in check_object["products"])

    assert len(data["products"]) == len(check_object["products"])
    for i, product in enumerate(data["products"]):
        assert product["name"] == check_object["products"][i]["name"]
        assert float(product["price"]) == float(check_object["products"][i]["price"])
        assert product["quantity"] == check_object["products"][i]["quantity"]
        assert float(product["total"]) == float(
            check_object["products"][i]["price"] * check_object["products"][i]["quantity"]
        )
    assert "links" in data
    assert "link_html" in data["links"]
    assert "link_txt" in data["links"]
    assert "link_qr" in data["links"]


@pytest.mark.asyncio
async def test_read_check_not_found(client: AsyncClient, token: str):
    """
    Test that attempting to retrieve a non-existent check returns a 404 error.
    """
    headers = {"Authorization": f"Bearer {token}"}

    non_existent_check_id = 99999

    response = await client.get(f"/api/check/find/{non_existent_check_id}", headers=headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text
    data = response.json()
    assert data["detail"] == f"Check ID: {non_existent_check_id} not found"


@pytest.mark.asyncio
async def test_get_checks_no_filters(client: AsyncClient, token: str, check_object: dict):
    """
    Test retrieving all checks without applying filters.
    """
    headers = {"Authorization": f"Bearer {token}"}

    for _ in range(3):
        response = await client.post("/api/check/", json=check_object, headers=headers)
        assert response.status_code == status.HTTP_201_CREATED, response.text

    response = await client.get("/api/check/select", headers=headers)
    assert response.status_code == status.HTTP_200_OK, response.text

    data = response.json()
    assert data["total"] >= 3
    assert len(data["entries"]) <= 10
    assert "entries" in data
    for check in data["entries"]:
        assert "id" in check
        assert "products" in check
        assert "payment" in check
        assert "total" in check
        assert "rest" in check
        assert "created_at" in check


@pytest.mark.asyncio
async def test_get_checks_with_filters(client: AsyncClient, token: str, check_object: dict):
    """
    Test retrieving checks with specific filters.
    """
    headers = {"Authorization": f"Bearer {token}"}

    check_object["payment"]["type"] = "cash"
    await client.post("/api/check/", json=check_object, headers=headers)

    check_object["payment"]["type"] = "cashless"
    await client.post("/api/check/", json=check_object, headers=headers)

    response = await client.get("/api/check/select?payment_type=cash", headers=headers)
    assert response.status_code == status.HTTP_200_OK, response.text

    data = response.json()
    assert data["total"] >= 1
    for check in data["entries"]:
        assert check["payment"]["type"] == "cash"


@pytest.mark.asyncio
async def test_get_checks_with_date_filters(client: AsyncClient, token: str, check_object: dict):
    """
    Test retrieving checks with date range filters.
    """
    headers = {"Authorization": f"Bearer {token}"}

    await client.post("/api/check/", json=check_object, headers=headers)

    date_from = (datetime.now() - timedelta(days=1)).isoformat()
    date_to = datetime.now().isoformat()

    response = await client.get(f"/api/check/select?createdAtFrom={date_from}&createdAtTo={date_to}", headers=headers)
    assert response.status_code == status.HTTP_200_OK, response.text

    # Validate the response
    data = response.json()
    assert data["total"] >= 1
    for check in data["entries"]:
        created_at = datetime.fromisoformat(check["created_at"])
        assert datetime.fromisoformat(date_from) <= created_at <= datetime.fromisoformat(date_to)


@pytest.mark.asyncio
async def test_get_checks_pagination(client: AsyncClient, token: str, check_object: dict):
    """
    Test retrieving checks with pagination.
    """
    headers = {"Authorization": f"Bearer {token}"}

    for _ in range(15):
        response = await client.post("/api/check/", json=check_object, headers=headers)
        assert response.status_code == status.HTTP_201_CREATED, response.text

    response = await client.get("/api/check/select?page=0&per_page=5", headers=headers)
    assert response.status_code == status.HTTP_200_OK, response.text
    data = response.json()
    assert len(data["entries"]) == 5
    assert data["page"] == 0
    assert data["per_page"] == 5

    response = await client.get("/api/check/select?page=1&per_page=5", headers=headers)
    assert response.status_code == status.HTTP_200_OK, response.text
    data = response.json()
    assert len(data["entries"]) == 5
    assert data["page"] == 1
    assert data["per_page"] == 5


@pytest.mark.asyncio
async def test_get_check_another_user(client: AsyncClient, token: str, check_object: dict, user):
    """
    Test that a user cannot access a check belonging to another user.
    """
    headers_user1 = {"Authorization": f"Bearer {token}"}

    response = await client.post("/api/check/", json=check_object, headers=headers_user1)
    assert response.status_code == status.HTTP_201_CREATED, response.text
    created_check = response.json()
    check_id = created_check["id"]

    # Create a second user
    second_user = {
        "username": "seconduser",
        "email": "seconduser@example.com",
        "password": "password123",
        "business_name": "FOP SecondUser"
    }
    await client.post("/api/auth/signup", json=second_user)
    login_response = await client.post(
        "/api/auth/login",
        json={"email": second_user["email"], "password": second_user["password"]}
    )
    assert login_response.status_code == status.HTTP_200_OK, login_response.text
    second_user_token = login_response.json()["access_token"]

    headers_user2 = {"Authorization": f"Bearer {second_user_token}"}

    response = await client.get(f"/api/check/find/{check_id}", headers=headers_user2)

    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text
    data = response.json()
    assert data["detail"] == f"Check ID: {check_id} not found"




