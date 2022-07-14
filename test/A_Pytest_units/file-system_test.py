import pytest
from copy import deepcopy
from test.data import db as data
from gudlft import filesystem
from gudlft.config import TestConfig


@pytest.fixture
def db():
    db = deepcopy(data)
    return db


class TestFileSystem:
    def test_settings(self):
        settings = filesystem.SETTINGS
        assert "tables" in settings.keys()
        keys = settings["tables"].keys()
        assert "clubs" in keys
        assert "competitions" in keys
        assert "bookings" in keys

    @pytest.mark.parametrize("table", ["clubs", "competitions"])
    def test_file_loading(self, table):
        data_list = filesystem.load_file(table, TestConfig.DATABASE)
        assert len(data_list) > 0
        assert isinstance(data_list[0], dict)

    def test_load_data(self, mocker):
        mocker.patch("gudlft.filesystem.load_file", return_value=[])
        db = filesystem.load_data()
        keys = db.keys()
        assert "clubs" in keys
        assert db["clubs"] == []
        assert "competitions" in keys
        assert "bookings" in keys

    def test_save_data(self, mocker, db):
        mocker.patch("gudlft.filesystem.save_to_file", return_value=True)
        filesystem.save_data(db)
        assert filesystem.save_to_file.call_count == 3

    def test_save_to_file(self, monkeypatch, db, tmp_path):
        filesystem.save_to_file("clubs", db["clubs"])
        filesystem.save_to_file("bookings", db["bookings"])
        assert len(list(tmp_path.iterdir())) == 2
