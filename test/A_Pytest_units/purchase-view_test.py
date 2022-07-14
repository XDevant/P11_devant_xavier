import pytest
from flask import current_app
from copy import deepcopy
from test.data import db as test_data
from test.mocks import mock_index_return
import gudlft


@pytest.fixture
def db():
    db = deepcopy(test_data)
    return db


@pytest.fixture
def form():
    form = {"competition": "bar", "club": "foo", "places": "8"}
    return form


class TestPurchaseView:
    def test_purchase_happy(self, client, mocker, form):
        mocker.patch('gudlft.filesystem.save_data')
        mocker.patch('gudlft.utils.find_index_by_key_value', mock_index_return)
        mocker.patch('gudlft.utils.get_booking', return_value=0)
        mocker.patch('gudlft.utils.set_booking')
        response = client.post('/purchasePlaces', data=form)
        assert response.status_code == 200
        # assert int(db["competitions"][0]['numberOfPlaces']) == 12
        # assert int(db["clubs"][0]["points"]) == 5

    @pytest.mark.parametrize("points, places", [(7, 9), (9, 7)])
    def test_purchase_sad_not_enough(self, app, client, mocker, points, places, form):
        with app.app_context():
            db = current_app.config['DB']
        db["clubs"][0]["points"] = str(points)
        db["competitions"][0]["numberOfPlaces"] = str(places)
        mocker.patch('gudlft.filesystem.save_data')
        mocker.patch('gudlft.utils.find_index_by_key_value', mock_index_return)
        mocker.patch('gudlft.utils.get_booking', return_value=0)
        mocker.patch('gudlft.utils.set_booking')
        response = client.post('/purchasePlaces', data=form)
        assert response.status_code == 200
        assert int(db["clubs"][0]["points"]) == points
        assert int(db["competitions"][0]['numberOfPlaces']) == places

    @pytest.mark.parametrize("amount", [-1, 13])
    def test_purchase_sad_purchase_out_of_range(self, app, client, mocker, amount, form):
        form["places"] = str(amount)
        mocker.patch('gudlft.filesystem.save_data')
        mocker.patch('gudlft.utils.find_index_by_key_value', mock_index_return)
        mocker.patch('gudlft.utils.get_booking', return_value=0)
        mocker.patch('gudlft.utils.set_booking')
        response = client.post('/purchasePlaces', data=form)
        with app.app_context():
            db = current_app.config['DB']
        assert response.status_code == 200
        assert int(db["competitions"][0]['numberOfPlaces']) == 20
        assert int(db["clubs"][0]["points"]) == 13

    def test_purchase_sad_previous_too_high(self, app, client, mocker, form):
        mocker.patch('gudlft.filesystem.save_data')
        mocker.patch('gudlft.utils.find_index_by_key_value', mock_index_return)
        mocker.patch('gudlft.utils.get_booking', return_value=8)
        mocker.patch('gudlft.utils.set_booking')
        with app.app_context():
            db = current_app.config['DB']
        db["bookings"][form["competition"]] = {form["club"]: form["places"]}
        assert int(db["competitions"][0]['numberOfPlaces']) == 20
        response = client.post('/purchasePlaces', data=form)
        assert response.status_code == 200
        assert int(db["clubs"][0]["points"]) == 13
        assert int(db["competitions"][0]['numberOfPlaces']) == 20
