import pytest
from copy import deepcopy
from test.data import db as data
from test.mocks import mock_index_return
import gudlft


@pytest.fixture
def db():
    db = deepcopy(data)
    return db


class TestBookingView:
    def test_booking_happy(self, client, mocker, db):
        mocker.patch.object(gudlft, 'data', db)
        mocker.patch('gudlft.utils.find_index_by_key_value', return_value=0)
        response = client.get('/book/bar/foo')
        assert response.status_code == 200
        assert "<h2>bar</h2>" in response.data.decode()

    def test_booking_sad_competition(self, client, mocker, db):
        mocker.patch.object(gudlft, 'data', db)
        mocker.patch('gudlft.utils.find_index_by_key_value', mock_index_return)
        response = client.get('/book/bir/foo')
        assert response.status_code == 200
        assert "Welcome, foo@foo.co" in response.data.decode()

    def test_booking_sad_club(self, client, mocker, db):
        mocker.patch.object(gudlft, 'data', db)
        mocker.patch('gudlft.utils.find_index_by_key_value', mock_index_return)
        response = client.get('/book/bar/foa')
        assert response.status_code == 302
        assert 'redirected automatically to target URL: <a href="/index">/index</a>' in response.data.decode()
