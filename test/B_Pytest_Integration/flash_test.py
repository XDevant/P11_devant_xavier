import pytest


class TestFlashErrorMessages:
    """Test messages sent back when data not found"""
    def test_booking_sad_competition(self, client):
        response = client.get('/book/bad/foo')
        assert response.status_code == 200
        assert "Something went wrong. Please try again" in response.data.decode()

    def test_booking_sad_club(self, client):
        response = client.get('/book/bar/fizz')
        assert response.status_code == 200
        assert 'Something went wrong. Please log again' in response.data.decode()
