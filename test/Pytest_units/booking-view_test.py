import pytest
from test.data import db as data
import server


@pytest.fixture
def db():
    db = data
    return db


class TestBookingView:
    def test_booking_happy(self, client, mocker, db):
        mocker.patch.object(server, 'data', db)
        response = client.get('/book/bar/foo')
        assert response.status_code == 200

    def test_booking_sad_competition(self, client, mocker, db):
        mocker.patch.object(server, 'data', db)
        response = client.get('/book/bir/foo')
        assert response.status_code == 200

    def test_booking_sad_club(self, client, mocker, db):
        mocker.patch.object(server, 'data', db)
        response = client.get('/book/bar/foa')
        assert response.status_code == 302
