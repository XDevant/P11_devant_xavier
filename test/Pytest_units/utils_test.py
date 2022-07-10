import pytest
from test.data import db as data
import server


@pytest.fixture
def db():
    db = data
    return db


class TestGetSetBooking:

    def test_get_booking_missing(self, mocker, db):
        mocker.patch.object(server, 'data', db)
        booked = server.get_booking("bar", "foo", db)
        assert booked == 0

    def test_set_booking_missing(self, mocker, db):
        mocker.patch.object(server, 'data', db)
        server.set_booking("bar", "foo", 2, db)
        assert int(server.data["bookings"]["bar"]["foo"]) == 2

    def test_get_booking_exist(self, mocker, db):
        db["bookings"]["bar"] = {"foo": 4}
        mocker.patch.object(server, 'data', db)
        booked = server.get_booking("bar", "foo", db)
        assert booked == 4

    def test_set_booking_exist(self, mocker, db):
        db["bookings"]["bar"] = {"foo": 4}
        mocker.patch.object(server, 'data', db)
        server.set_booking("bar", "foo", 6, db)
        assert int(server.data["bookings"]["bar"]["foo"]) == 6
