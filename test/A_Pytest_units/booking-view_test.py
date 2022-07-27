from test.data import db as test_data
from test.mocks import mock_index_return
import gudlft


class TestBookingView:
    def test_booking_happy(self, client, mocker):
        mocker.patch('gudlft.utils.find_index_by_key_value', return_value=0)
        response = client.get('/book/bar/foo')
        assert response.status_code == 200
        content = response.data.decode()
        assert "<h2>bar</h2>" in content
        assert ">Places available:" in content
        assert ">Points available:" in content

    def test_booking_sad_competition(self, client, mocker):
        mocker.patch('gudlft.utils.find_index_by_key_value', mock_index_return)
        response = client.get('/book/bad/foo')
        assert response.status_code == 200
        assert "Welcome, foo@foo.co" in response.data.decode()

    def test_booking_sad_club(self, client, mocker):
        mocker.patch('gudlft.utils.find_index_by_key_value', mock_index_return)
        response = client.get('/book/bar/fizz')
        assert response.status_code == 200
        assert 'Welcome to the GUDLFT Registration Portal!' in response.data.decode()
