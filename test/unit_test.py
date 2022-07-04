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


class TestBookingView:
    clubs = [{
        "name": "Simply Lift",
        "email": "john@simplylift.co",
        "points": "13"
    }]
    competitions = [{
            "name": "Spring Festival",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25"
        }]

    def test_login_happy(self, client, mocker):
        mocker.patch.object(server, 'clubs', self.clubs)
        mocker.patch.object(server, 'competitions', self.competitions)
        response = client.get('/book/Spring Festival/Simply Lift')
        assert response.status_code == 200

    def test_login_sad_competition(self, client, mocker):
        mocker.patch.object(server, 'clubs', self.clubs)
        mocker.patch.object(server, 'competitions', self.competitions)
        response = client.get('/book/Spring Festival/SimplyLift')
        assert response.status_code == 200

    def test_login_sad_club(self, client, mocker):
        mocker.patch.object(server, 'clubs', self.clubs)
        mocker.patch.object(server, 'competitions', self.competitions)
        response = client.get('/book/SpringFestival/Simply Lift')
        assert response.status_code == 200


class TestPurchaseView:
    pass
