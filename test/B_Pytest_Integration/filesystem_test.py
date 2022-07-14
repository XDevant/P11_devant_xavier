import pytest
from flask import current_app
from copy import deepcopy
from test.data import db as test_data
from gudlft import filesystem


@pytest.fixture
def db():
    db = deepcopy(test_data)
    return db


class TestFileSystem:
    def test_load_data(self, app):
        with app.app_context():
            db = filesystem.load_data()
        assert db.keys() == {"competitions", "clubs", "bookings"}
        assert len(db["clubs"]) > 0
        assert isinstance(db["bookings"], dict)

    def test_save_load_data(self, db, app):
        with app.app_context():
            filesystem.save_data(db)
            new_db = filesystem.load_data()
            path = current_app.config['DATABASE']
        assert new_db == db
        assert path == './test/Temp'
