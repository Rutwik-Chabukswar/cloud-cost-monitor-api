import pytest
from app.core.config import settings

def test_create_resource_unauthorized(client):
    """Ensure POST to /resources requires authentication."""
    resource_data = {"name": "Test-EC2", "service_type": "EC2", "unit_price": 0.05}
    response = client.post(f"{settings.API_V1_STR}/resources/", json=resource_data)
    assert response.status_code == 401 # Unauthorized

def test_create_resource_authorized(client, test_user):
    """Test authorized resource creation."""
    headers = {"Authorization": test_user["Authorization"]}
    resource_data = {"name": "Test-S3", "service_type": "S3", "unit_price": 0.01}
    
    response = client.post(
        f"{settings.API_V1_STR}/resources/", 
        json=resource_data, 
        headers=headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == resource_data["name"]
    assert "id" in data

def test_list_resources(client):
    """Test public access to resource listing."""
    response = client.get(f"{settings.API_V1_STR}/resources/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_delete_resource_authorized(client, test_user):
    """Test authorized resource deletion."""
    headers = {"Authorization": test_user["Authorization"]}
    
    # First create a resource
    resource_data = {"name": "Delete-Me", "service_type": "RDS", "unit_price": 0.10}
    create_response = client.post(
        f"{settings.API_V1_STR}/resources/", 
        json=resource_data, 
        headers=headers
    )
    resource_id = create_response.json()["id"]
    
    # Then delete it
    delete_response = client.delete(
        f"{settings.API_V1_STR}/resources/{resource_id}", 
        headers=headers
    )
    
    assert delete_response.status_code == 200
    assert "deleted" in delete_response.json()["message"]
