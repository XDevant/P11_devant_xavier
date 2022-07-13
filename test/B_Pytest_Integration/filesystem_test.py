import pytest
from copy import deepcopy
from test.data import db as data
from gudlft import views


@pytest.fixture
def db():
    db = deepcopy(data)
    return db


class TestFileSystem:
    def test_load_data(self):
        db = server.load_data()
        assert db.keys() == {"competitions", "clubs", "bookings"}
        assert len(db["clubs"]) > 0
        assert isinstance(db["bookings"], dict)

    def test_save_load_data(self, monkeypatch, db, tmp_path):
        monkeypatch.setitem(server.SETTINGS, "path", str(tmp_path) + "/")
        server.save_data(db)
        assert len(list(tmp_path.iterdir())) == 3
        new_db = server.load_data()
        assert new_db == db
