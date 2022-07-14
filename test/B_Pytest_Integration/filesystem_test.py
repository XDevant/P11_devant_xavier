import pytest
from copy import deepcopy
from test.data import db as test_data
from gudlft import filesystem


@pytest.fixture
def db():
    db = deepcopy(data)
    return db


class TestFileSystem:
    def test_load_data(self):
        db = filesystem.load_data()
        assert db.keys() == {"competitions", "clubs", "bookings"}
        assert len(db["clubs"]) > 0
        assert isinstance(db["bookings"], dict)

    def test_save_load_data(self, tmp_path):
        filesystem.save_data(db)
        assert len(list(tmp_path.iterdir())) == 3
        new_db = filesystem.load_data()
        assert new_db == db
