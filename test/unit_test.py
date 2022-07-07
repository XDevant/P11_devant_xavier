import server


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

    def test_booking_happy(self, client, mocker):
        mocker.patch.object(server, 'clubs', self.clubs)
        mocker.patch.object(server, 'competitions', self.competitions)
        response = client.get('/book/Spring Festival/Simply Lift')
        assert response.status_code == 200

    def test_booking_sad_competition(self, client, mocker):
        mocker.patch.object(server, 'clubs', self.clubs)
        mocker.patch.object(server, 'competitions', self.competitions)
        response = client.get('/book/SpringFestival/Simply Lift')
        assert response.status_code == 200

    def test_booking_sad_club(self, client, mocker):
        mocker.patch.object(server, 'clubs', self.clubs)
        mocker.patch.object(server, 'competitions', self.competitions)
        response = client.get('/book/Spring Festival/SimplyLift')
        assert response.status_code == 302


class TestPurchaseView:
    clubs = [{
        "name": "Simply Lift",
        "email": "john@simplylift.co",
        "points": "13"
    }]
    competitions = [{
        "name": "Spring Festival",
        "date": "2020-03-27 10:00:00",
        "numberOfPlaces": "5"
    }]

    def test_purchase_happy(self, client, mocker):
        data = {'competition': 'Spring Festival',
                'club': 'Simply Lift',
                'places': 4}
        mocker.patch.object(server, 'clubs', self.clubs)
        mocker.patch.object(server, 'competitions', self.competitions)
        response = client.post('/purchasePlaces', data=data)
        assert response.status_code == 200
        assert self.competitions[0]['numberOfPlaces'] == 1

    def test_purchase_sad_not_enough_places(self, client, mocker):
        data = {'competition': 'Spring Festival',
                'club': 'Simply Lift',
                'places': 6}
        mocker.patch.object(server, 'clubs', self.clubs)
        mocker.patch.object(server, 'competitions', self.competitions)
        response = client.post('/purchasePlaces', data=data)
        assert response.status_code == 200
        assert self.competitions[0]['numberOfPlaces'] >= 0

    def test_purchase_sad_negative_purchase(self, client, mocker):
        data = {'competition': 'Spring Festival',
                'club': 'Simply Lift',
                'places': -1}
        mocker.patch.object(server, 'clubs', self.clubs)
        mocker.patch.object(server, 'competitions', self.competitions)
        response = client.post('/purchasePlaces', data=data)
        assert response.status_code == 200
        assert self.competitions[0]['numberOfPlaces'] == 1


class TestRankingView:
    clubs = [{"name": "Foo", "email": "foo@foo.co", "points": "13"},
             {"name": "Bar", "email": "bar@bar.co", "points": "20"}
             ]

    def test_ranking_status_code_ok(self, client, mocker):
        mocker.patch.object(server, 'clubs', self.clubs)
        response = client.get('/ranking')
        assert response.status_code == 200
