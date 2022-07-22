import pytest
from test.data import db as data
import gudlft


class TestHomeView:
    def test_login_happy(self, client, mocker):
        form = {'email': data["clubs"][0]["email"]}
        mocker.patch('gudlft.utils.shutdown_server')
        mocker.patch('gudlft.utils.find_index_by_key_value', return_value=0)
        response = client.post('/showSummary', data=form)
        assert response.status_code == 200
        assert gudlft.utils.shutdown_server.call_count == 0
        content = response.data.decode()
        assert f'h2>Welcome, {data["clubs"][0]["email"]}</h2' in content
        assert f'>Points available: {data["clubs"][0]["points"]}' in content

    def test_login_sad(self, client, mocker):
        form = {'email': 'foo@bar.co'}
        mocker.patch('gudlft.utils.shutdown_server')
        mocker.patch('gudlft.utils.find_index_by_key_value', return_value=-1)
        with pytest.raises(RuntimeError):
            response = client.post('/showSummary', data=form)
            assert response.status_code == 500
