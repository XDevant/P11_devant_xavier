class TestBookingJson:
    """Test json file loading and booking view"""
    def test_booking_happy(self, client):
        response = client.get('/book/Spring Festival/Simply Lift')
        assert response.status_code == 200

    def test_booking_sad_competition(self, client):
        response = client.get('/book/SpringFestival/Simply Lift')
        assert response.status_code == 200

    def test_booking_sad_club(self, client):
        response = client.get('/book/Spring Festival/SimplyLift')
        assert response.status_code == 302
