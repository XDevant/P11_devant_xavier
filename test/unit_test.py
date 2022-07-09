import server
import pytest


class TestDataBase:
    def test_load_clubs(self):
        club_list = server.load_clubs()
        assert len(club_list) > 0

    def test_load_competitions(self):
        competition_list = server.load_competitions()
        assert len(competition_list) > 0

    def test_update_clubs(self):
        server.save_clubs(server.clubs)
        club_list = server.load_clubs()
        assert club_list == server.clubs

    def test_update_competitions(self):
        server.save_competitions(server.competitions)
        competition_list = server.load_competitions()
        assert competition_list == server.competitions


class TestLandingView:
    def test_index_status_code_ok(self, client):
        response = client.get('/')
        assert response.status_code == 200

    def test_logout_status_code_ok(self, client):
        response = client.get('/logout')
        assert response.status_code == 302


class TestLoginView:
    clubs = [{
        "name": "FooBar",
        "email": "foo@bar.co",
        "points": "13"
    }]

    def test_login_happy(self, client, mocker):
        data = {'email': 'foo@bar.co'}
        mocker.patch.object(server, 'clubs', self.clubs)
        response = client.post('/showSummary', data=data)
        assert response.status_code == 200
        assert f"Welcome, {data['email']}" in response.data.decode()

    def test_login_sad(self, client, mocker):
        data = {'email': 'j@s.co'}
        mocker.patch.object(server, 'clubs', self.clubs)
        response = client.post('/showSummary', data=data)
        assert response.data.decode() == "<h1>Server shutting down...</h1>"


class TestBookingView:
    clubs = [{
        "name": "foo",
        "email": "foo@sfoo.co",
        "points": "13"
    }]
    competitions = [{
            "name": "bar",
            "date": "?",
            "numberOfPlaces": "25",
            "orders": {}
        }]

    def test_booking_happy(self, client, mocker):
        mocker.patch.object(server, 'clubs', self.clubs)
        mocker.patch.object(server, 'competitions', self.competitions)
        response = client.get('/book/bar/foo')
        assert response.status_code == 200

    def test_booking_sad_competition(self, client, mocker):
        mocker.patch.object(server, 'clubs', self.clubs)
        mocker.patch.object(server, 'competitions', self.competitions)
        response = client.get('/book/bir/foo')
        assert response.status_code == 200

    def test_booking_sad_club(self, client, mocker):
        mocker.patch.object(server, 'clubs', self.clubs)
        mocker.patch.object(server, 'competitions', self.competitions)
        response = client.get('/book/bar/foa')
        assert response.status_code == 302


class TestPurchaseView:
    clubs = [{"name": "foo", "points": 0}]
    competitions = [{"name": "bar", "numberOfPlaces": 0, "orders": {}}]
    order = {'competition': 'bar', 'club': 'foo', 'places': 0}

    def setup(self, method):
        if method == "test_purchase_sad_not_enough_places_or_points":
            self.competitions[0]["numberOfPlaces"] = 7
            self.order["places"] = 8
            print(f"Trying to buy 8 places while only 7 points/places left")
        else:
            self.clubs[0]["points"] = 13
            self.competitions[0]["numberOfPlaces"] = 20
            print(f"Trying to buy n places with enough points/places left")

    def test_purchase_happy(self, client, mocker):
        self.order["places"] = 8
        mocker.patch.object(server, 'clubs', self.clubs)
        mocker.patch.object(server, 'competitions', self.competitions)
        mocker.patch('server.save_clubs', return_value=None)
        mocker.patch('server.save_competitions', return_value=None)
        response = client.post('/purchasePlaces', data=self.order)
        assert response.status_code == 200
        assert self.competitions[0]['numberOfPlaces'] == 12
        assert self.clubs[0]["points"] == 5

    @pytest.mark.parametrize("points, places", [(7, 9), (9, 7)])
    def test_purchase_sad_not_enough(self, client, mocker, points, places):
        self.clubs[0]["points"] = points
        self.competitions[0]["numberOfPlaces"] = places
        mocker.patch.object(server, 'clubs', self.clubs)
        mocker.patch.object(server, 'competitions', self.competitions)
        mocker.patch('server.save_clubs', return_value=None)
        mocker.patch('server.save_competitions', return_value=None)
        response = client.post('/purchasePlaces', data=self.order)
        assert response.status_code == 200
        assert self.clubs[0]["points"] == points
        assert self.competitions[0]['numberOfPlaces'] == places

    @pytest.mark.parametrize("amount", [-1, 13])
    def test_purchase_sad_purchase_out_of_range(self, client, mocker, amount):
        self.order["places"] = amount
        mocker.patch.object(server, 'clubs', self.clubs)
        mocker.patch.object(server, 'competitions', self.competitions)
        mocker.patch('server.save_clubs', return_value=None)
        mocker.patch('server.save_competitions', return_value=None)
        response = client.post('/purchasePlaces', data=self.order)
        assert response.status_code == 200
        assert self.competitions[0]['numberOfPlaces'] == 20
        assert self.clubs[0]["points"] == 13


class TestRankingView:
    clubs = [{"name": "Foo", "email": "foo@foo.co", "points": "3"},
             {"name": "Bar", "email": "bar@bar.co", "points": "20"}
             ]

    def test_ranking_status_code_ok(self, client, mocker):
        mocker.patch.object(server, 'clubs', self.clubs)
        response = client.get('/ranking')
        data = response.data.decode()
        assert response.status_code == 200
        assert f"{self.clubs[0]['name']} Points: {self.clubs[0]['points']}" in data
        assert f"{self.clubs[1]['name']} Points: {self.clubs[1]['points']}" in data
