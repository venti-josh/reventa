import pytest
import asyncio
from httpx import AsyncClient


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def async_client():
    """Async client for testing the API endpoints."""
    import importlib
    try:
        app = importlib.import_module("app.main").app
        async with AsyncClient(app=app, base_url="http://test") as client:
            yield client
    except (ModuleNotFoundError, AttributeError):
        pytest.skip("FastAPI app not yet implemented")


@pytest.fixture
def auth_header():
    """Returns a dummy authorization header.
    
    TODO: Replace with real auth implementation later.
    """
    return {"Authorization": "Bearer dummy"} 