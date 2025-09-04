import importlib
import pytest
from httpx import AsyncClient

try:
    app = importlib.import_module("app.main").app  # type: ignore
except (ModuleNotFoundError, AttributeError):
    pytest.skip("FastAPI app not yet implemented", allow_module_level=True)


@pytest.mark.xfail(reason="endpoint not implemented")  # TODO: Remove after implementation
async def test_create_survey(async_client: AsyncClient, auth_header):
    """Test creating a new survey."""
    payload = {
        "title": "Customer Satisfaction Survey",
        "description": "Survey to gather feedback from event attendees",
        "questions": [
            {
                "type": "multiple_choice",
                "text": "How would you rate the event?",
                "options": ["Excellent", "Good", "Average", "Poor"]
            },
            {
                "type": "text",
                "text": "What did you like most about the event?",
            }
        ]
    }
    
    response = await async_client.post("/surveys", json=payload, headers=auth_header)
    
    assert response.status_code == 201
    data = response.json()
    assert set(data.keys()) >= {"id", "title", "description", "questions", "created_at", "status"}
    assert data["status"] == "draft"
    assert len(data["questions"]) == len(payload["questions"])


@pytest.mark.xfail(reason="endpoint not implemented")  # TODO: Remove after implementation
async def test_get_surveys(async_client: AsyncClient, auth_header):
    """Test retrieving all surveys."""
    response = await async_client.get("/surveys", headers=auth_header)
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        assert set(data[0].keys()) >= {"id", "title", "created_at", "status"}


@pytest.mark.parametrize(
    "survey_id,status_code",
    [
        ("123e4567-e89b-12d3-a456-426614174000", 200),  # Valid UUID
        ("999", 404),  # Not found
    ],
)
@pytest.mark.xfail(reason="endpoint not implemented")  # TODO: Remove after implementation
async def test_get_survey_by_id(async_client: AsyncClient, auth_header, survey_id, status_code):
    """Test retrieving a specific survey by ID."""
    response = await async_client.get(f"/surveys/{survey_id}", headers=auth_header)
    
    assert response.status_code == status_code
    if status_code == 200:
        data = response.json()
        assert set(data.keys()) >= {
            "id", "title", "description", "questions", 
            "created_at", "updated_at", "status"
        }
        assert isinstance(data["questions"], list)


@pytest.mark.xfail(reason="endpoint not implemented")  # TODO: Remove after implementation
async def test_update_survey(async_client: AsyncClient, auth_header):
    """Test updating an existing survey."""
    survey_id = "123e4567-e89b-12d3-a456-426614174000"
    payload = {
        "title": "Updated Survey Title",
        "questions": [
            {
                "id": "q1",
                "text": "Updated question text",
            }
        ]
    }
    
    response = await async_client.patch(f"/surveys/{survey_id}", json=payload, headers=auth_header)
    
    assert response.status_code == 200
    data = response.json()
    assert set(data.keys()) >= {"id", "title", "questions", "updated_at"}
    assert data["title"] == payload["title"]


@pytest.mark.parametrize(
    "survey_id,status_code",
    [
        ("123e4567-e89b-12d3-a456-426614174000", 200),  # Valid UUID, draft survey
        ("223e4567-e89b-12d3-a456-426614174000", 400),  # Valid UUID, already published survey
        ("999", 404),  # Not found
    ],
)
@pytest.mark.xfail(reason="endpoint not implemented")  # TODO: Remove after implementation
async def test_publish_survey(async_client: AsyncClient, auth_header, survey_id, status_code):
    """Test publishing a survey."""
    response = await async_client.post(f"/surveys/{survey_id}/publish", headers=auth_header)
    
    assert response.status_code == status_code
    if status_code == 200:
        data = response.json()
        assert set(data.keys()) >= {"id", "status", "published_at"}
        assert data["status"] == "published"


@pytest.mark.xfail(reason="endpoint not implemented")  # TODO: Remove after implementation
async def test_surveys_unauthorized(async_client: AsyncClient):
    """Test accessing surveys without authorization."""
    # Test GET all
    response = await async_client.get("/surveys")
    assert response.status_code == 401
    
    # Test GET one
    response = await async_client.get("/surveys/123e4567-e89b-12d3-a456-426614174000")
    assert response.status_code == 401
    
    # Test POST
    response = await async_client.post("/surveys", json={"title": "Test"})
    assert response.status_code == 401 