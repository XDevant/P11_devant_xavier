import pytest
from copy import deepcopy
from test.data import db as data
from test.mocks import mock_index_return
import server


@pytest.fixture
def db():
    db = deepcopy(data)
    return db


class TestBookingFileSystemn:
    """Test json file loading and booking view"""
    def test_booking_happy(self, client, mocker, monkeypatch, db, tmp_path):
        monkeypatch.setitem(server.SETTINGS, "path", str(tmp_path) + "/")
        server.save_data(db)
        new_db = server.load_data()
        mocker.patch.object(server, 'data', new_db)
        mocker.patch('server.find_index_by_key_value', mock_index_return)
        response = client.get('/book/bar/foo')
        assert response.status_code == 200
        assert "<h2>bar</h2>" in response.data.decode()

    def test_booking_sad_competition(self, client, mocker, monkeypatch, db, tmp_path):
        monkeypatch.setitem(server.SETTINGS, "path", str(tmp_path) + "/")
        server.save_data(db)
        new_db = server.load_data()
        mocker.patch.object(server, 'data', new_db)
        mocker.patch('server.find_index_by_key_value', mock_index_return)
        response = client.get('/book/bam/foo')
        assert response.status_code == 200
        assert "<h2>Welcome, foo@foo.co" in response.data.decode()

    def test_booking_sad_club(self, client, mocker, monkeypatch, db, tmp_path):
        monkeypatch.setitem(server.SETTINGS, "path", str(tmp_path) + "/")
        server.save_data(db)
        new_db = server.load_data()
        mocker.patch.object(server, 'data', new_db)
        mocker.patch('server.find_index_by_key_value', mock_index_return)
        response = client.get('/book/bar/fizz')
        assert response.status_code == 302
        assert 'redirected automatically to target URL: <a href="/index">/index</a>' in response.data.decode()


class TestBookingIndexFinder:
    """Test json file loading and booking view"""
    def test_booking_happy(self, client, mocker, db):
        mocker.patch.object(server, 'data', db)
        response = client.get('/book/bar/foo')
        assert response.status_code == 200
        assert "<h2>bar</h2>" in response.data.decode()

    def test_booking_sad_competition(self, client, mocker, db):
        mocker.patch.object(server, 'data', db)
        response = client.get('/book/bam/foo')
        assert response.status_code == 200
        assert "<h2>Welcome, foo@foo.co" in response.data.decode()

    def test_booking_sad_club(self, client, mocker, db):
        mocker.patch.object(server, 'data', db)
        response = client.get('/book/bar/fizz')
        assert response.status_code == 302
        assert 'redirected automatically to target URL: <a href="/index">/index</a>' in response.data.decode()
