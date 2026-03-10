import logging
from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password, verify_password

logger = logging.getLogger("cloud-cost-monitor")

def create_user(db: Session, user_in: UserCreate) -> User:
    """Register a new user in the system."""
    logger.info(f"Registering new user: {user_in.email}")
    db_user = User(
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
        is_active=user_in.is_active
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Retrieve a user by their primary key."""
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Retrieve a user by their email address."""
    return db.query(User).filter(User.email == email).first()

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """Authenticate a user and verify their credentials."""
    logger.info(f"Authenticating user: {email}")
    user = get_user_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
