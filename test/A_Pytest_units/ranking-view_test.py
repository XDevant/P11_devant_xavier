import pytest
from test.data import db as data
from gudlft import views


@pytest.fixture
def db():
    db = data
    return db


class TestRankingView:
    def test_ranking_status_code_ok(self, client, mocker, db):
        mocker.patch.object(server, 'data', db)
        response = client.get('/ranking')
        new_db = response.data.decode()
        assert response.status_code == 200
        assert f'{db["clubs"][0]["name"]} Points: {db["clubs"][0]["points"]}' in new_db
        assert f'{db["clubs"][1]["name"]} Points: {db["clubs"][1]["points"]}' in new_db
