import importlib
import pytest
from httpx import AsyncClient

try:
    app = importlib.import_module("app.main").app  # type: ignore
except (ModuleNotFoundError, AttributeError):
    pytest.skip("FastAPI app not yet implemented", allow_module_level=True)


@pytest.mark.xfail(reason="endpoint not implemented")  # TODO: Remove after implementation
async def test_create_event(async_client: AsyncClient, auth_header):
    """Test creating a new event."""
    payload = {
        "name": "Annual Conference 2023",
        "description": "Our annual tech conference",
        "start_date": "2023-10-15T09:00:00Z",
        "end_date": "2023-10-17T18:00:00Z",
        "location": "San Francisco, CA"
    }
    
    response = await async_client.post("/events", json=payload, headers=auth_header)
    
    assert response.status_code == 201
    data = response.json()
    assert set(data.keys()) >= {"id", "name", "description", "start_date", "end_date", "location", "created_at"}


@pytest.mark.xfail(reason="endpoint not implemented")  # TODO: Remove after implementation
async def test_get_events(async_client: AsyncClient, auth_header):
    """Test retrieving all events."""
    response = await async_client.get("/events", headers=auth_header)
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        assert set(data[0].keys()) >= {"id", "name", "start_date", "end_date", "created_at"}


@pytest.mark.parametrize(
    "event_id,status_code",
    [
        ("123e4567-e89b-12d3-a456-426614174000", 200),  # Valid UUID
        ("999", 404),  # Not found
        ("invalid-id", 422),  # Invalid UUID format
    ],
)
@pytest.mark.xfail(reason="endpoint not implemented")  # TODO: Remove after implementation
async def test_get_event_by_id(async_client: AsyncClient, auth_header, event_id, status_code):
    """Test retrieving a specific event by ID."""
    response = await async_client.get(f"/events/{event_id}", headers=auth_header)
    
    assert response.status_code == status_code
    if status_code == 200:
        data = response.json()
        assert set(data.keys()) >= {
            "id", "name", "description", "start_date", "end_date", 
            "location", "created_at", "updated_at"
        }


@pytest.mark.xfail(reason="endpoint not implemented")  # TODO: Remove after implementation
async def test_update_event(async_client: AsyncClient, auth_header):
    """Test updating an existing event."""
    event_id = "123e4567-e89b-12d3-a456-426614174000"
    payload = {
        "name": "Updated Conference Name",
        "location": "New York, NY"
    }
    
    response = await async_client.patch(f"/events/{event_id}", json=payload, headers=auth_header)
    
    assert response.status_code == 200
    data = response.json()
    assert set(data.keys()) >= {"id", "name", "description", "location", "updated_at"}
    assert data["name"] == payload["name"]
    assert data["location"] == payload["location"]


@pytest.mark.parametrize(
    "event_id,status_code",
    [
        ("123e4567-e89b-12d3-a456-426614174000", 204),  # Valid UUID
        ("999", 404),  # Not found
    ],
)
@pytest.mark.xfail(reason="endpoint not implemented")  # TODO: Remove after implementation
async def test_delete_event(async_client: AsyncClient, auth_header, event_id, status_code):
    """Test deleting an event."""
    response = await async_client.delete(f"/events/{event_id}", headers=auth_header)
    
    assert response.status_code == status_code


@pytest.mark.xfail(reason="endpoint not implemented")  # TODO: Remove after implementation
async def test_events_unauthorized(async_client: AsyncClient):
    """Test accessing events without authorization."""
    # Test GET all
    response = await async_client.get("/events")
    assert response.status_code == 401
    
    # Test GET one
    response = await async_client.get("/events/123e4567-e89b-12d3-a456-426614174000")
    assert response.status_code == 401
    
    # Test POST
    response = await async_client.post("/events", json={"name": "Test"})
    assert response.status_code == 401 