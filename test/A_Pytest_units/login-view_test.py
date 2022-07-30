class TestLoginView:
    def test_index_status_code_ok(self, client):
        response = client.get('/')
        assert response.status_code == 200

    def test_logout_status_code_ok(self, client):
        response = client.get('/logout')
        assert response.status_code == 200

    def test_login_form_has_input_submit(self, client):
        response = client.get('/')
        html = response.data.decode()
        assert '<input type="email"' in html
        assert '<button type="submit"' in html
