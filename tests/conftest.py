import pytest
from fastapi.testclient import TestClient
from database import get_redis_client
from main import app


@pytest.fixture
def test_client():
    client = TestClient(app)
    client.app.dependency_overrides[get_redis_client] = get_redis_client
    return client
