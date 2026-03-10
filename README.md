# Cloud Resource Cost Monitoring API

A production-ready FastAPI backend for tracking cloud resource usage and cost analytics.

## Features

- **Resource Management**: Create, view, and list cloud resources (EC2, S3, RDS, etc.).
- **Usage Tracking**: Record hourly usage for specific resources.
- **Cost Analytics**: Summarize costs by service type and identify top expensive resources.
- **Containerized Integration**: One-command deployment with Docker Compose.
- **Health Monitoring**: Advanced observability with Docker healthchecks and service dependencies.
- **Production-Ready Core**:
  - Environment Configuration: Pydantic settings with `.env` support.
  - Health Monitoring: Dedicated health check endpoint with DB connectivity verification.
  - Structured Logging: Request/Response middleware and detailed operation logs.
  - Global Error Handling: Centralized exception management for clean API response.
  - Rich API Docs: Enhanced Swagger UI metadata with tags and descriptions.

---

## 🚀 Getting Started with Docker (Recommended)

The easiest way to run the API and its PostgreSQL database is using **Docker Compose**.

### 1. Prerequisites
- Docker installed
- Docker Compose installed

### 2. Run the System
Navigate to the project root and execute:

```bash
docker-compose up --build
```

The system will:
1.  **Initialize PostgreSQL**: Create a containerized database (`cloud_cost_db`).
2.  **Wait for Database**: Use a healthcheck to ensure the database is ready before starting the API.
3.  **Start FastAPI**: Build the lightweight Python container and start the backend.

- **API URL**: [http://localhost:8000](http://localhost:8000)
- **Swagger Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Health Check**: [http://localhost:8000/api/v1/health/](http://localhost:8000/api/v1/health/)

---

## 🛠 Manual Installation (Optional Local Development)

### 1. Prerequisites
- Python 3.8+
- PostgreSQL (optional, defaults to SQLite)

### 2. Setup
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Start Server
```bash
uvicorn app.main:app --reload
```

## Monitoring & Analytics

- **Health Monitoring**: `GET /api/v1/health/`
- **Analytics - Top Expensive**: `GET /api/v1/analytics/top-expensive`
- **Analytics - Service Summary**: `GET /api/v1/analytics/service-summary`

## Authentication

The API uses JWT (JSON Web Tokens) for authentication.

### 1. Register a User
**POST `/api/v1/auth/register`**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

### 2. Login
**POST `/api/v1/auth/login`**
Use `application/x-www-form-urlencoded` with fields:
- `username`: your email
- `password`: your password

**Sample Response**:
```json
{
  "access_token": "eyJhbG...",
  "token_type": "bearer"
}
```

### 3. Using Protected Routes
For routes like `POST /api/v1/resources/` or `POST /api/v1/usage/`, include the token in the headers:
`Authorization: Bearer <your_access_token>`
