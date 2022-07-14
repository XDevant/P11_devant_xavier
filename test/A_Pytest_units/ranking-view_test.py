from test.data import db as test_data


class TestRankingView:
    def test_ranking_status_code_ok(self, client):
        response = client.get('/ranking')
        content = response.data.decode()
        assert response.status_code == 200
        assert f'{test_data["clubs"][0]["name"]} Points: {test_data["clubs"][0]["points"]}' in content
        assert f'{test_data["clubs"][1]["name"]} Points: {test_data["clubs"][1]["points"]}' in content
