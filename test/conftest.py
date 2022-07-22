import pytest
from copy import deepcopy
from gudlft import create_app
from test.data import db
from gudlft.config import PytestConfig


@pytest.fixture()
def app():
    app = create_app(config_class=PytestConfig)
    return app


@pytest.fixture(scope='function')
def client(app):
    """client app"""
    app.config.update({'DB': deepcopy(db)})
    with app.test_client() as client:
        yield client


@pytest.fixture
def form():
    form = {"competition": "bar", "club": "foo", "places": "8", "email": "foo@foo.co"}
    return form
