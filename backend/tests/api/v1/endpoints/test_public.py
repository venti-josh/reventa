import importlib
import pytest
from httpx import AsyncClient

try:
    app = importlib.import_module("app.main").app  # type: ignore
except (ModuleNotFoundError, AttributeError):
    pytest.skip("FastAPI app not yet implemented", allow_module_level=True)


@pytest.mark.parametrize(
    "link_uuid,status_code",
    [
        ("123e4567-e89b-12d3-a456-426614174000", 200),  # Valid UUID
        ("999", 404),  # Not found
        ("expired-link-uuid", 410),  # Expired link
    ],
)
@pytest.mark.xfail(reason="endpoint not implemented")  # TODO: Remove after implementation
async def test_get_public_survey(async_client: AsyncClient, link_uuid, status_code):
    """Test retrieving a public survey form by link UUID."""
    response = await async_client.get(f"/l/{link_uuid}")
    
    assert response.status_code == status_code
    if status_code == 200:
        data = response.json()
        assert set(data.keys()) >= {"survey", "recipient"}
        assert set(data["survey"].keys()) >= {"title", "description", "questions"}
        assert isinstance(data["survey"]["questions"], list)


@pytest.mark.parametrize(
    "link_uuid,status_code",
    [
        ("123e4567-e89b-12d3-a456-426614174000", 201),  # Valid UUID
        ("999", 404),  # Not found
        ("expired-link-uuid", 410),  # Expired link
        ("already-submitted-uuid", 400),  # Already submitted
    ],
)
@pytest.mark.xfail(reason="endpoint not implemented")  # TODO: Remove after implementation
async def test_submit_public_survey(async_client: AsyncClient, link_uuid, status_code):
    """Test submitting responses to a public survey."""
    payload = {
        "responses": [
            {
                "question_id": "q1",
                "answer": "Excellent"
            },
            {
                "question_id": "q2",
                "answer": "The speakers were very engaging and informative."
            }
        ]
    }
    
    response = await async_client.post(f"/l/{link_uuid}/submit", json=payload)
    
    assert response.status_code == status_code
    if status_code == 201:
        data = response.json()
        assert set(data.keys()) >= {"id", "submitted_at", "message"}
        assert "success" in data["message"].lower()


@pytest.mark.xfail(reason="endpoint not implemented")  # TODO: Remove after implementation
async def test_submit_invalid_responses(async_client: AsyncClient):
    """Test submitting invalid responses to a public survey."""
    link_uuid = "123e4567-e89b-12d3-a456-426614174000"
    payload = {
        "responses": [
            {
                "question_id": "q1",
                # Missing answer
            },
            {
                "question_id": "invalid-question",
                "answer": "This won't work"
            }
        ]
    }
    
    response = await async_client.post(f"/l/{link_uuid}/submit", json=payload)
    
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data 