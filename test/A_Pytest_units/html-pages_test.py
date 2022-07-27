import pytest


class TestPages:
    @pytest.mark.parametrize("endpoint, method", [('/', 'GET'), ('/ranking', 'GET'), ('/book/bar/foo', 'GET'),
                                                  ('/showSummary', 'POST'),
                                                  ('/ranking?club=foo', 'GET'),
                                                  ('/ranking?club=foo&competition=bar', 'GET')])
    def test_endpoint_has_nav(self, client, endpoint, method, form):
        if method == "GET":
            response = client.get(endpoint)
        else:
            response = client.post(endpoint, data=form)
        html = response.data.decode()
        assert "<nav>" in html
        assert "</a>" in html
        if '/ranking' not in endpoint:
            assert '<a href="/ranking' in html
            if endpoint != '/':
                assert "Logout" in html
        elif endpoint == '/ranking':
            assert "Login" in html
        else:
            assert '<a href="/showSummary' in html
