import pytest
from copy import deepcopy
from test.data import db as data
import server


@pytest.fixture
def db():
    db = deepcopy(data)
    return db


class TestFileSystem:
    def test_settings(self):
        settings = server.SETTINGS
        assert "path" in settings.keys()
        assert "tables" in settings.keys()
        keys = settings["tables"].keys()
        assert "clubs" in keys
        assert "competitions" in keys
        assert "bookings" in keys

    @pytest.mark.parametrize("table", ["clubs", "competitions"])
    def test_file_loading(self, table):
        data_list = server.load_file(table)
        assert len(data_list) > 0
        assert isinstance(data_list[0], dict)

    def test_load_data(self, mocker):
        mocker.patch("server.load_file", return_value=[])
        db = server.load_data()
        keys = db.keys()
        assert "clubs" in keys
        assert db["clubs"] == []
        assert "competitions" in keys
        assert "bookings" in keys

    def test_save_data(self, mocker, db):
        mocker.patch("server.save_to_file", return_value=True)
        server.save_data(db)
        assert server.save_to_file.call_count == 3

    def test_save_to_file(self, monkeypatch, db, tmp_path):
        monkeypatch.setitem(server.SETTINGS, "path", str(tmp_path) + "/")
        server.save_to_file("clubs", db["clubs"])
        server.save_to_file("bookings", db["bookings"])
        assert len(list(tmp_path.iterdir())) == 2
