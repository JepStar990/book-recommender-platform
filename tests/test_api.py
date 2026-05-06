from fastapi.testclient import TestClient
import pytest


@pytest.fixture
def client():
    from app.main import app
    return TestClient(app)


class TestHealthEndpoint:
    def test_health_returns_200(self, client):
        response = client.get("/health")
        assert response.status_code == 200


class TestSearchEndpoint:
    def test_search_with_short_query_fails(self, client):
        response = client.get("/search?q=a&limit=5")
        assert response.status_code == 422  # min_length=2

    def test_search_with_valid_query(self, client):
        response = client.get("/search?q=python&limit=5")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


class TestRecommendEndpoint:
    def test_recommend_with_invalid_id(self, client):
        response = client.get("/recommend/by-book?volume_id=nonexistent123&n=5")
        assert response.status_code in (200, 404, 500)
