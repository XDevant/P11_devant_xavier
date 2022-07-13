import pytest
from test.data import db as data
from gudlft import views
from copy import deepcopy


@pytest.fixture
def db():
    db = deepcopy(data)
    return db


class TestHomeView:

    def test_login_happy(self, client, mocker, db):
        form = {'email': 'foo@foo.co'}
        mocker.patch.object(server, 'data', db)
        mocker.patch('server.shutdown_server')
        mocker.patch('server.find_index_by_key_value', return_value=0)
        response = client.post('/showSummary', data=form)
        assert response.status_code == 200
        assert server.shutdown_server.call_count == 0
        assert "Welcome, foo@foo.co" in response.data.decode()

    def test_login_sad(self, client, mocker, db):
        form = {'email': 'foo@bar.co'}
        mocker.patch.object(server, 'data', db)
        mocker.patch('server.shutdown_server')
        mocker.patch('server.find_index_by_key_value', return_value=-1)
        response = client.post('/showSummary', data=form)
        assert response.data.decode() == "<h1>Server shutting down...</h1>"
        assert server.shutdown_server.call_count == 1
