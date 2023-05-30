import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def test_app():
    with TestClient(app) as client:
        yield client
