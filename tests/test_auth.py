import pytest
from app.core.config import settings

def test_register_user(client):
    """Test user registration."""
    user_data = {"email": "newuser@example.com", "password": "securepassword"}
    response = client.post(f"{settings.API_V1_STR}/auth/register", json=user_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_data["email"]
    assert "id" in data

def test_login_user(client):
    """Test user login and token generation."""
    # First register
    user_data = {"email": "loginuser@example.com", "password": "securepassword"}
    client.post(f"{settings.API_V1_STR}/auth/register", json=user_data)
    
    # Then login
    login_data = {"username": user_data["email"], "password": user_data["password"]}
    response = client.post(f"{settings.API_V1_STR}/auth/login", data=login_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials(client):
    """Test login failure with bad credentials."""
    login_data = {"username": "wrong@example.com", "password": "wrongpassword"}
    response = client.post(f"{settings.API_V1_STR}/auth/login", data=login_data)
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect email or password"
