from test.data import db as data


class TestHomeView:
    def test_login_happy(self, client, mocker):
        form = {'email': data["clubs"][0]["email"]}
        mocker.patch('gudlft.utils.find_index_by_key_value', return_value=0)
        response = client.post('/showSummary', data=form)
        assert response.status_code == 200
        content = response.data.decode()
        assert f'h2>Welcome, {data["clubs"][0]["email"]}</h2' in content
        assert f'>Points available: {data["clubs"][0]["points"]}' in content

    def test_login_sad(self, client, mocker):
        form = {'email': 'foo@bar.co'}
        mocker.patch('gudlft.utils.find_index_by_key_value', return_value=-1)
        response = client.post('/showSummary', data=form)
        assert response.status_code == 200
        assert 'Welcome to the GUDLFT Registration Portal!' in response.data.decode()

    def test_back_home(self, client, mocker):
        form = {'club': data["clubs"][0]["name"]}
        mocker.patch('gudlft.utils.find_index_by_key_value', return_value=0)
        response = client.post('/showSummary', data=form)
        assert response.status_code == 200
        content = response.data.decode()
        assert f'h2>Welcome, {data["clubs"][0]["email"]}</h2' in content
