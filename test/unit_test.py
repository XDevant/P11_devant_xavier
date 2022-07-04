from test.conftest import client


def test_index_status_code_ok(client):
    response = client.get('/')
    assert response.status_code == 200


def test_login_happy(client):
    data = {'email': 'john@simplylift.co'}
    response = client.post('/showSummary', data=data)
    data = response.data.decode()
    assert response.status_code == 200
    assert 'Welcome, john@simplylift.co' in data


def test_login_sad(client):
    data = {'email': 'j@s.co'}
    response = client.post('/showSummary', data=data)
    data = response.data.decode()
    assert response.status_code == 200
    assert 'Welcome to the GUDLFT Registration Portal' in data
