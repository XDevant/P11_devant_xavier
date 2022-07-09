import pytest
from server import app


@pytest.fixture
def client():
    """client app"""
    app.testing = True
    with app.test_client() as client:
        yield client
