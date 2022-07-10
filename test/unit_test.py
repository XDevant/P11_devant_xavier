import server
import pytest


@pytest.fixture
def data_fixture():
    db = {"clubs": [{
                     "name": "foo",
                     "email": "foo@foo.co",
                     "points": "13"
                    }],
          "competitions": [{
                            "name": "bar",
                            "date": "?",
                            "numberOfPlaces": "25",
                           }],
          "bookings": {}
          }
    return db


@pytest.fixture
def purchase_data_fixt():
    db = {
          "clubs": [{"name": "foo", "points": "13"}],
          "competitions": [{"name": "bar", "numberOfPlaces": "20"}],
          "bookings": {
                       "bar": {"foo": "0"}
                       }
          }
    return db


@pytest.fixture
def purchase_form_fixt():
    form = {"competition": "bar", "club": "foo", "places": "8"}
    return form


class TestFileSystem:

    def setup_method(self, method):
        pass

    def test_settings(self):
        settings = server.SETTINGS
        assert "path" in settings.keys()
        assert "tables" in settings.keys()
        keys = settings["tables"].keys()
        assert "clubs" in keys
        assert "competitions" in keys
        assert "bookings" in keys

    @pytest.mark.parametrize("table", ["clubs", "competitions"])
    def test_file_loading(self, table):
        data_list = server.load_file(table)
        assert len(data_list) > 0
        assert isinstance(data_list[0], dict)

    def test_load_data(self, mocker):
        mocker.patch("server.load_file", return_value=[])
        db = server.load_data()
        keys = db.keys()
        assert "clubs" in keys
        assert db["clubs"] == []
        assert "competitions" in keys
        assert "bookings" in keys

    def test_save_data(self, mocker, data_fixture):
        mocker.patch("server.save_to_file", return_value=True)
        server.save_data(data_fixture)
        assert server.save_to_file.call_count == 3

    def test_save_to_file(self):
        pass


class TestLandingView:
    def test_index_status_code_ok(self, client):
        response = client.get('/')
        assert response.status_code == 200

    def test_logout_status_code_ok(self, client):
        response = client.get('/logout')
        assert response.status_code == 302


class TestLoginView:

    def test_login_happy(self, client, mocker, data_fixture):
        form = {'email': 'foo@foo.co'}
        mocker.patch.object(server, 'data', data_fixture)
        response = client.post('/showSummary', data=form)
        assert response.status_code == 200
        assert "Welcome, foo@foo.co" in response.data.decode()

    def test_login_sad(self, client, mocker, data_fixture):
        form = {'email': 'foo@bar.co'}
        mocker.patch.object(server, 'data', data_fixture)
        mocker.patch('server.shutdown_server')
        response = client.post('/showSummary', data=form)
        assert response.data.decode() == "<h1>Server shutting down...</h1>"
        assert server.shutdown_server.call_count == 1


class TestBookingView:

    def test_booking_happy(self, client, mocker, data_fixture):
        mocker.patch.object(server, 'data', data_fixture)
        response = client.get('/book/bar/foo')
        assert response.status_code == 200

    def test_booking_sad_competition(self, client, mocker, data_fixture):
        mocker.patch.object(server, 'data', data_fixture)
        response = client.get('/book/bir/foo')
        assert response.status_code == 200

    def test_booking_sad_club(self, client, mocker, data_fixture):
        mocker.patch.object(server, 'data', data_fixture)
        response = client.get('/book/bar/foa')
        assert response.status_code == 302


class TestPurchaseView:

    def test_purchase_happy(self, client, mocker, purchase_data_fixt, purchase_form_fixt):
        mocker.patch.object(server, 'data', purchase_data_fixt)
        mocker.patch('server.save_data')
        mocker.patch('server.get_booking', return_value=0)
        mocker.patch('server.set_booking')
        response = client.post('/purchasePlaces', data=purchase_form_fixt)
        assert response.status_code == 200
        assert int(purchase_data_fixt["competitions"][0]['numberOfPlaces']) == 12
        assert int(purchase_data_fixt["clubs"][0]["points"]) == 5

    @pytest.mark.parametrize("points, places", [(7, 9), (9, 7)])
    def test_purchase_sad_not_enough(self, client, mocker, points, places, purchase_data_fixt, purchase_form_fixt):
        purchase_data_fixt["clubs"][0]["points"] = str(points)
        purchase_data_fixt["competitions"][0]["numberOfPlaces"] = str(places)
        mocker.patch.object(server, 'data', purchase_data_fixt)
        mocker.patch('server.save_data')
        mocker.patch('server.get_booking', return_value=0)
        mocker.patch('server.set_booking')
        response = client.post('/purchasePlaces', data=purchase_form_fixt)
        assert response.status_code == 200
        assert int(purchase_data_fixt["clubs"][0]["points"]) == points
        assert int(purchase_data_fixt["competitions"][0]['numberOfPlaces']) == places

    @pytest.mark.parametrize("amount", [-1, 13])
    def test_purchase_sad_purchase_out_of_range(self, client, mocker, amount, purchase_data_fixt, purchase_form_fixt):
        purchase_form_fixt["places"] = str(amount)
        mocker.patch.object(server, 'data', purchase_data_fixt)
        mocker.patch('server.save_data')
        mocker.patch('server.get_booking', return_value=0)
        mocker.patch('server.set_booking')
        response = client.post('/purchasePlaces', data=purchase_form_fixt)
        assert response.status_code == 200
        assert int(purchase_data_fixt["competitions"][0]['numberOfPlaces']) == 20
        assert int(purchase_data_fixt["clubs"][0]["points"]) == 13

    def test_purchase_sad_previous_too_high(self, client, mocker, purchase_data_fixt, purchase_form_fixt):
        mocker.patch.object(server, 'data', purchase_data_fixt)
        mocker.patch('server.save_data')
        mocker.patch('server.get_booking', return_value=8)
        mocker.patch('server.set_booking')
        response = client.post('/purchasePlaces', data=purchase_form_fixt)
        assert response.status_code == 200
        assert int(purchase_data_fixt["competitions"][0]['numberOfPlaces']) == 20
        assert int(purchase_data_fixt["clubs"][0]["points"]) == 13


class TestRankingView:
    data = {"clubs": [{"name": "Foo", "email": "foo@foo.co", "points": "3"},
                      {"name": "Bar", "email": "bar@bar.co", "points": "20"}
                      ]
            }

    def test_ranking_status_code_ok(self, client, mocker):
        mocker.patch.object(server, 'data', self.data)
        response = client.get('/ranking')
        data = response.data.decode()
        assert response.status_code == 200
        assert f'{self.data["clubs"][0]["name"]} Points: {self.data["clubs"][0]["points"]}' in data
        assert f'{self.data["clubs"][1]["name"]} Points: {self.data["clubs"][1]["points"]}' in data
