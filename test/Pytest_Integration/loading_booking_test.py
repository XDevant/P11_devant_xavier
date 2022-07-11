import pytest
from test.data import db as data
import server


@pytest.fixture
def db():
    db = data
    return db


class TestBookingJson:
    """Test json file loading and booking view"""
    def test_booking_happy(self, client, mocker, monkeypatch, db, tmp_path):
        monkeypatch.setitem(server.SETTINGS, "path", str(tmp_path) + "/")
        server.save_data(db)
        new_db = server.load_data()
        mocker.patch.object(server, 'data', new_db)
        response = client.get('/book/bar/foo')
        assert response.status_code == 200

    def test_booking_sad_competition(self, client, mocker, monkeypatch, db, tmp_path):
        monkeypatch.setitem(server.SETTINGS, "path", str(tmp_path) + "/")
        server.save_data(db)
        new_db = server.load_data()
        mocker.patch.object(server, 'data', new_db)
        response = client.get('/book/bam/foo')
        assert response.status_code == 200

    def test_booking_sad_club(self, client, mocker, monkeypatch, db, tmp_path):
        monkeypatch.setitem(server.SETTINGS, "path", str(tmp_path) + "/")
        server.save_data(db)
        new_db = server.load_data()
        mocker.patch.object(server, 'data', new_db)
        response = client.get('/book/bar/fizz')
        assert response.status_code == 302
