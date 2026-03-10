import pytest
from app.core.config import settings

def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get(f"{settings.API_V1_STR}/health/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "database" in data
    assert "timestamp" in data
