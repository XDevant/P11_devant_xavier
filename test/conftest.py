import pytest
from flask import Config
from gudlft import create_app


class TestConfig(Config):
    SECRET_KEY = 'top-secret-key'
    JSONIFY_PRETTYPRINT_REGULAR = True
    DATABASE = "./test/Temp/"
    TESTING = True
    LIVESERVER_PORT = '8000'


@pytest.fixture()
def app():
    app, d = create_app(config_class=TestConfig)
    return app


@pytest.fixture
def client(app):
    """client app"""
    with app.test_client() as client:
        yield client
