import pytest
from flask import Config
from gudlft import create_app
from test.data import db


class TestConfig(Config):
    SECRET_KEY = 'top-secret-key'
    JSONIFY_PRETTYPRINT_REGULAR = True
    TESTING = True
    DATABASE = "./test/JSON/"
    TEMP = "./test/Temp/"
    DB = db
    LIVESERVER_PORT = '8001'


@pytest.fixture
def app():
    app = create_app(config_class=TestConfig)
    return app


@pytest.fixture
def client(app):
    """client app"""
    app.config['DB'] = db
    with app.test_client() as client:
        yield client
