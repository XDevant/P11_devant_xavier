import pytest
from flask import current_app
from gudlft import filesystem


class TestFileSystem:
    def test_settings(self):
        settings = filesystem.SETTINGS
        assert "tables" in settings.keys()
        keys = settings["tables"].keys()
        assert "clubs" in keys
        assert "competitions" in keys
        assert "bookings" in keys

    @pytest.mark.parametrize("table", ["clubs", "competitions"])
    def test_file_loading(self, app, table):
        with app.app_context():
            data_list = filesystem.load_file(table)
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

    def test_save_data(self, mocker, app):
        mocker.patch("gudlft.filesystem.save_to_file", return_value=True)
        with app.app_context():
            db = current_app.config['DB']
            filesystem.save_data(db)
            path = current_app.config['DATABASE']
        assert filesystem.save_to_file.call_count == 3
        assert path == './test/Temp'

    def test_save_to_file(self, app):
        with app.app_context():
            db = current_app.config['DB']
            filesystem.save_to_file("clubs", db["clubs"])
            filesystem.save_to_file("bookings", db["bookings"])
            path = current_app.config['DATABASE']
        assert path == './test/Temp'
        # assert len(list(tmp_path.iterdir())) == 2
