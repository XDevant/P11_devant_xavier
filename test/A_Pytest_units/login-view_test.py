class TestLoginView:
    def test_index_status_code_ok(self, client):
        response = client.get('/')
        assert response.status_code == 200

    def test_logout_status_code_ok(self, client):
        response = client.get('/logout')
        assert response.status_code == 302
