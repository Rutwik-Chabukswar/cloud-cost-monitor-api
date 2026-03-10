from app.db.session import get_db

# Dependency to get db session - re-exporting for better modularity in api routes
__all__ = ["get_db"]
