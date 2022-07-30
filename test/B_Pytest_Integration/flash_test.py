
class TestFlashErrorMessages:
    """Test messages sent back when data not found"""
    def test_booking_sad_competition(self, client):
        response = client.get('/book/bad/foo')
        assert response.status_code == 200
        assert "Ressource indisponible ou inexistante." in response.data.decode()

    def test_booking_sad_club(self, client):
        response = client.get('/book/bar/fizz')
        assert response.status_code == 200
        assert 'Session expirée, veuillez vous reconnecter' in response.data.decode()

    def test_login_sad_email(self, client):
        form = {'email': 'foo@bar.co'}
        response = client.post('/showSummary', data=form)
        assert response.status_code == 200
        assert 'Désolé, couriel non trouvé.' in response.data.decode()
