from flask import current_app
from test.mocks import mock_index_return
from gudlft import filesystem


class TestBookingFileSystem:
    """Test json file loading and booking view"""
    def test_booking_happy(self, client, mocker):
        filesystem.save_data(current_app.config['DB'])
        new_db = filesystem.load_data()
        current_app.config['DB'] = new_db
        mocker.patch('gudlft.views.find_index_by_key_value', mock_index_return)
        response = client.get('/book/bar/foo')
        assert response.status_code == 200
        assert "<h2>bar</h2>" in response.data.decode()

    def test_booking_sad_competition(self, client, mocker):
        filesystem.save_data(current_app.config['DB'])
        new_db = filesystem.load_data()
        current_app.config['DB'] = new_db
        mocker.patch('gudlft.views.find_index_by_key_value', mock_index_return)
        response = client.get('/book/bam/foo')
        assert response.status_code == 200
        assert "<h2>Welcome, foo@foo.co" in response.data.decode()

    def test_booking_sad_club(self, client, mocker):
        filesystem.save_data(current_app.config['DB'])
        new_db = filesystem.load_data()
        current_app.config['DB'] = new_db
        mocker.patch('gudlft.views.find_index_by_key_value', mock_index_return)
        response = client.get('/book/bar/fizz')
        assert response.status_code == 200
        assert 'Welcome to the GUDLFT Registration Portal!' in response.data.decode()


class TestBookingIndexFinder:
    """Test json file loading and booking view"""
    def test_booking_happy(self, client):
        response = client.get('/book/bar/foo')
        assert response.status_code == 200
        assert "<h2>bar</h2>" in response.data.decode()

    def test_booking_sad_competition(self, client):
        response = client.get('/book/bam/foo')
        assert response.status_code == 200
        assert "<h2>Welcome, foo@foo.co" in response.data.decode()

    def test_booking_sad_club(self, client):
        response = client.get('/book/bar/fizz')
        assert response.status_code == 200
        assert 'Welcome to the GUDLFT Registration Portal!' in response.data.decode()
