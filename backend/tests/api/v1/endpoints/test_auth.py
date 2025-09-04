import importlib
import pytest
from httpx import AsyncClient

try:
    app = importlib.import_module("app.main").app  # type: ignore
except (ModuleNotFoundError, AttributeError):
    pytest.skip("FastAPI app not yet implemented", allow_module_level=True)


@pytest.mark.xfail(reason="endpoint not implemented")  # TODO: Remove after implementation
async def test_register(async_client: AsyncClient):
    """Test user registration for org admin."""
    payload = {
        "email": "admin@example.com",
        "password": "strongpassword123",
        "name": "Admin User",
        "organization_name": "Test Organization"
    }
    
    response = await async_client.post("/auth/register", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert set(data.keys()) >= {"id", "email", "name", "organization"}
    assert set(data["organization"].keys()) >= {"id", "name"}


@pytest.mark.parametrize(
    "payload,status_code",
    [
        (
            {"email": "user@example.com", "password": "password123"},
            200,
        ),
        (
            {"email": "nonexistent@example.com", "password": "wrongpassword"},
            401,
        ),
        (
            {"email": "invalid_format", "password": "password123"},
            422,
        ),
    ],
)
@pytest.mark.xfail(reason="endpoint not implemented")  # TODO: Remove after implementation
async def test_login(async_client: AsyncClient, payload, status_code):
    """Test user login with various scenarios."""
    response = await async_client.post("/auth/jwt/login", data=payload)
    
    assert response.status_code == status_code
    if status_code == 200:
        data = response.json()
        assert set(data.keys()) >= {"access_token", "refresh_token", "token_type"}
        assert data["token_type"] == "bearer"


@pytest.mark.xfail(reason="endpoint not implemented")  # TODO: Remove after implementation
async def test_refresh_token(async_client: AsyncClient):
    """Test refreshing JWT token."""
    payload = {"refresh_token": "some-refresh-token"}
    
    response = await async_client.post("/auth/jwt/refresh", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert set(data.keys()) >= {"access_token", "token_type"}
    assert data["token_type"] == "bearer"


@pytest.mark.xfail(reason="endpoint not implemented")  # TODO: Remove after implementation
async def test_refresh_token_invalid(async_client: AsyncClient):
    """Test refreshing with invalid token."""
    payload = {"refresh_token": "invalid-token"}
    
    response = await async_client.post("/auth/jwt/refresh", json=payload)
    
    assert response.status_code == 401 