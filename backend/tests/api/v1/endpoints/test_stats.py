import importlib
import pytest
from httpx import AsyncClient

try:
    app = importlib.import_module("app.main").app  # type: ignore
except (ModuleNotFoundError, AttributeError):
    pytest.skip("FastAPI app not yet implemented", allow_module_level=True)


@pytest.mark.parametrize(
    "event_id,status_code",
    [
        ("123e4567-e89b-12d3-a456-426614174000", 200),  # Valid UUID
        ("999", 404),  # Not found
    ],
)
@pytest.mark.xfail(reason="endpoint not implemented")  # TODO: Remove after implementation
async def test_get_event_stats(async_client: AsyncClient, auth_header, event_id, status_code):
    """Test retrieving statistics for a specific event."""
    response = await async_client.get(f"/events/{event_id}/stats", headers=auth_header)
    
    assert response.status_code == status_code
    if status_code == 200:
        data = response.json()
        assert set(data.keys()) >= {
            "event_id", "total_surveys", "total_responses", 
            "response_rate", "surveys", "latest_responses"
        }
        assert isinstance(data["surveys"], list)
        if data["surveys"]:
            assert set(data["surveys"][0].keys()) >= {
                "id", "title", "responses_count", "completion_rate"
            }


@pytest.mark.parametrize(
    "survey_id,status_code",
    [
        ("123e4567-e89b-12d3-a456-426614174000", 200),  # Valid UUID
        ("999", 404),  # Not found
    ],
)
@pytest.mark.xfail(reason="endpoint not implemented")  # TODO: Remove after implementation
async def test_export_survey_responses(async_client: AsyncClient, auth_header, survey_id, status_code):
    """Test exporting responses for a specific survey."""
    response = await async_client.get(f"/surveys/{survey_id}/responses/export", headers=auth_header)
    
    assert response.status_code == status_code
    if status_code == 200:
        # Check that we receive a CSV content type
        assert response.headers["content-type"] == "text/csv"
        # Check that the CSV content is not empty
        assert len(response.content) > 0
        # First line should be header row with at least these columns
        first_line = response.content.decode("utf-8").splitlines()[0]
        assert all(col in first_line for col in ["response_id", "submitted_at", "question", "answer"])


@pytest.mark.xfail(reason="endpoint not implemented")  # TODO: Remove after implementation
async def test_stats_unauthorized(async_client: AsyncClient):
    """Test accessing statistics without authorization."""
    # Test event stats
    event_id = "123e4567-e89b-12d3-a456-426614174000"
    response = await async_client.get(f"/events/{event_id}/stats")
    assert response.status_code == 401
    
    # Test survey export
    survey_id = "123e4567-e89b-12d3-a456-426614174000"
    response = await async_client.get(f"/surveys/{survey_id}/responses/export")
    assert response.status_code == 401 