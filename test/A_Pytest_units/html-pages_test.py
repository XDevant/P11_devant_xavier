import pytest


class TestPages:
    @pytest.mark.parametrize("endpoint", ['/', '/ranking', '/purchasePlaces', '/showSummary'])
    def test_endpoint_has_nav(self, client, endpoint):
        response = client.get(endpoint)
        html = response.data.decode()
        assert "<nav>" in html
        assert "</a>" in html
