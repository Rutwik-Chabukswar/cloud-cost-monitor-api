import pytest
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.api.deps import get_db
from app.db.session import Base
from app.main import app
from app.core.config import settings

# Test database setup (Always use SQLite for isolated tests)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_db():
    # Create tables
    Base.metadata.create_all(bind=engine)
    yield
    # Cleanup after session
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db() -> Generator:
    # Transactional database session for each test
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(db) -> Generator:
    # Override get_db dependency
    def override_get_db():
        try:
            yield db
        finally:
            pass
            
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

@pytest.fixture
def test_user(client):
    # Register and login a test user
    user_data = {"email": "test@example.com", "password": "testpassword123"}
    client.post(f"{settings.API_V1_STR}/auth/register", json=user_data)
    
    login_data = {"username": user_data["email"], "password": user_data["password"]}
    response = client.post(f"{settings.API_V1_STR}/auth/login", data=login_data)
    
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}", "email": user_data["email"]}
