import server
import pytest


@pytest.fixture
def db():
    db = {"clubs": [{
                     "name": "foo",
                     "email": "foo@foo.co",
                     "points": "13"
                    },
                    {
                     "name": "fuu",
                     "email": "fuu@fuu.co",
                     "points": "15"
                    }],
          "competitions": [{
                            "name": "bar",
                            "date": "?",
                            "numberOfPlaces": "20",
                           }],
          "bookings": {}
          }
    return db


@pytest.fixture
def form():
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

    def test_save_data(self, mocker, db):
        mocker.patch("server.save_to_file", return_value=True)
        server.save_data(db)
        assert server.save_to_file.call_count == 3

    def test_save_to_file(self, monkeypatch, db, tmp_path):
        monkeypatch.setitem(server.SETTINGS, "path", str(tmp_path) + "/")
        server.save_to_file("clubs", db["clubs"])
        server.save_to_file("bookings", db["bookings"])
        assert len(list(tmp_path.iterdir())) == 2


class TestLandingView:
    def test_index_status_code_ok(self, client):
        response = client.get('/')
        assert response.status_code == 200

    def test_logout_status_code_ok(self, client):
        response = client.get('/logout')
        assert response.status_code == 302


class TestLoginView:

    def test_login_happy(self, client, mocker, db):
        form = {'email': 'foo@foo.co'}
        mocker.patch.object(server, 'data', db)
        response = client.post('/showSummary', data=form)
        assert response.status_code == 200
        assert "Welcome, foo@foo.co" in response.data.decode()

    def test_login_sad(self, client, mocker, db):
        form = {'email': 'foo@bar.co'}
        mocker.patch.object(server, 'data', db)
        mocker.patch('server.shutdown_server')
        response = client.post('/showSummary', data=form)
        assert response.data.decode() == "<h1>Server shutting down...</h1>"
        assert server.shutdown_server.call_count == 1


class TestBookingView:

    def test_booking_happy(self, client, mocker, db):
        mocker.patch.object(server, 'data', db)
        response = client.get('/book/bar/foo')
        assert response.status_code == 200

    def test_booking_sad_competition(self, client, mocker, db):
        mocker.patch.object(server, 'data', db)
        response = client.get('/book/bir/foo')
        assert response.status_code == 200

    def test_booking_sad_club(self, client, mocker, db):
        mocker.patch.object(server, 'data', db)
        response = client.get('/book/bar/foa')
        assert response.status_code == 302


class TestPurchaseView:

    def test_purchase_happy(self, client, mocker, db, form):
        mocker.patch.object(server, 'data', db)
        mocker.patch('server.save_data')
        mocker.patch('server.get_booking', return_value=0)
        mocker.patch('server.set_booking')
        response = client.post('/purchasePlaces', data=form)
        assert response.status_code == 200
        assert int(db["competitions"][0]['numberOfPlaces']) == 12
        assert int(db["clubs"][0]["points"]) == 5

    @pytest.mark.parametrize("points, places", [(7, 9), (9, 7)])
    def test_purchase_sad_not_enough(self, client, mocker, points, places, db, form):
        db["clubs"][0]["points"] = str(points)
        db["competitions"][0]["numberOfPlaces"] = str(places)
        mocker.patch.object(server, 'data', db)
        mocker.patch('server.save_data')
        mocker.patch('server.get_booking', return_value=0)
        mocker.patch('server.set_booking')
        response = client.post('/purchasePlaces', data=form)
        assert response.status_code == 200
        assert int(db["clubs"][0]["points"]) == points
        assert int(db["competitions"][0]['numberOfPlaces']) == places

    @pytest.mark.parametrize("amount", [-1, 13])
    def test_purchase_sad_purchase_out_of_range(self, client, mocker, amount, db, form):
        form["places"] = str(amount)
        mocker.patch.object(server, 'data', db)
        mocker.patch('server.save_data')
        mocker.patch('server.get_booking', return_value=0)
        mocker.patch('server.set_booking')
        response = client.post('/purchasePlaces', data=form)
        assert response.status_code == 200
        assert int(db["competitions"][0]['numberOfPlaces']) == 20
        assert int(db["clubs"][0]["points"]) == 13

    def test_purchase_sad_previous_too_high(self, client, mocker, db, form):
        mocker.patch.object(server, 'data', db)
        mocker.patch('server.save_data')
        mocker.patch('server.get_booking', return_value=8)
        mocker.patch('server.set_booking')
        response = client.post('/purchasePlaces', data=form)
        assert response.status_code == 200
        assert int(db["competitions"][0]['numberOfPlaces']) == 20
        assert int(db["clubs"][0]["points"]) == 13


class TestRankingView:

    def test_ranking_status_code_ok(self, client, mocker, db):
        mocker.patch.object(server, 'data', db)
        response = client.get('/ranking')
        data = response.data.decode()
        assert response.status_code == 200
        assert f'{db["clubs"][0]["name"]} Points: {db["clubs"][0]["points"]}' in data
        assert f'{db["clubs"][1]["name"]} Points: {db["clubs"][1]["points"]}' in data
