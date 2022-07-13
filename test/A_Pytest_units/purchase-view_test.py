import pytest
from copy import deepcopy
from test.data import db as data
from test.mocks import mock_index_return
from gudlft import views


@pytest.fixture
def db():
    db = deepcopy(data)
    return db


@pytest.fixture
def form():
    form = {"competition": "bar", "club": "foo", "places": "8"}
    return form


class TestPurchaseView:
    def test_purchase_happy(self, client, mocker, db, form):
        mocker.patch.object(server, 'data', db)
        mocker.patch('server.save_data')
        mocker.patch('server.find_index_by_key_value', mock_index_return)
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
        mocker.patch('server.find_index_by_key_value', mock_index_return)
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
        mocker.patch('server.find_index_by_key_value', mock_index_return)
        mocker.patch('server.get_booking', return_value=0)
        mocker.patch('server.set_booking')
        response = client.post('/purchasePlaces', data=form)
        assert response.status_code == 200
        assert int(db["competitions"][0]['numberOfPlaces']) == 20
        assert int(db["clubs"][0]["points"]) == 13

    def test_purchase_sad_previous_too_high(self, client, mocker, db, form):
        mocker.patch.object(server, 'data', db)
        mocker.patch('server.save_data')
        mocker.patch('server.find_index_by_key_value', mock_index_return)
        mocker.patch('server.get_booking', return_value=8)
        mocker.patch('server.set_booking')
        response = client.post('/purchasePlaces', data=form)
        assert response.status_code == 200
        assert int(db["competitions"][0]['numberOfPlaces']) == 20
        assert int(db["clubs"][0]["points"]) == 13
