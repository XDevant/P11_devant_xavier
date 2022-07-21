import pytest


class TestPages:
    @pytest.mark.parametrize("endpoint, method", [('/', 'GET'), ('/ranking', 'GET'), ('/showSummary', 'POST'),
                                                  ('/book/bar/foo', 'GET')])
    def test_endpoint_has_nav(self, client, endpoint, method, form):
        if method == "GET":
            response = client.get(endpoint)
        else:
            response = client.post(endpoint, data=form)
        html = response.data.decode()
        assert "<nav>" in html
        assert "</a>" in html
        if endpoint != '/ranking':
            assert "Go to gudlft ranking page" in html
            if endpoint != '/':
                assert "logout" in html
        else:
            assert "Go back to loging page" in html
