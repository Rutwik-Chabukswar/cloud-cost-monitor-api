import pytest
from app.core.config import settings

def test_record_usage_authorized(client, test_user):
    """Test authorized usage recording."""
    headers = {"Authorization": test_user["Authorization"]}
    
    # Create required resource first
    resource_data = {"name": "Usage-EC2", "service_type": "EC2", "unit_price": 0.05}
    create_response = client.post(
        f"{settings.API_V1_STR}/resources/", 
        json=resource_data, 
        headers=headers
    )
    resource_id = create_response.json()["id"]
    
    # Record usage
    usage_data = {"resource_id": resource_id, "hours": 10.5}
    response = client.post(
        f"{settings.API_V1_STR}/usage/", 
        json=usage_data, 
        headers=headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["resource_id"] == resource_id
    assert data["hours"] == usage_data["hours"]
    assert "id" in data

def test_record_usage_unauthorized(client):
    """Ensure recording usage requires authentication."""
    usage_data = {"resource_id": 1, "hours": 5.0} # Even for non-existent resource
    response = client.post(f"{settings.API_V1_STR}/usage/", json=usage_data)
    assert response.status_code == 401
