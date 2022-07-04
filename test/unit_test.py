from test.conftest import client
import server


def test_index_status_code_ok(client):
    response = client.get('/')
    assert response.status_code == 200


class TestLoginViews:
    clubs = [{
        "name": "Simply Lift",
        "email": "john@simplylift.co",
        "points": "13"
    }]

    def test_login_happy(self, client, mocker):
        data = {'email': 'john@simplylift.co'}
        mocker.patch.object(server, 'clubs', self.clubs)
        response = client.post('/showSummary', data=data)
        assert response.status_code == 200
        assert f"Welcome, {data['email']}" in response.data.decode()

    def test_login_sad(self, client, mocker):
        data = {'email': 'j@s.co'}
        mocker.patch.object(server, 'clubs', self.clubs)
        response = client.post('/showSummary', data=data)
        assert response.status_code == 302
