# Cloud Resource Cost Monitoring API

A production-ready FastAPI backend for tracking cloud resource usage and cost analytics.

## Features

- **Resource Management**: Create, view, and list cloud resources (EC2, S3, RDS, etc.) with custom hourly rates.
- **Usage Tracking**: Record hourly usage for specific resources.
- **Cost Analytics**:
  - Individual resource total cost calculation.
  - Service-wide cost summaries.
  - Identification of most expensive resources.
- **Database Support**: Built-in support for PostgreSQL and SQLite (fallback for local development).

## Project Structure

```text
app/
├── api/             # API routes and dependencies
│   └── v1/          # Version 1 of the API
├── core/            # App configurations and core settings
├── crud/            # Database operations (CRUD)
├── db/              # Database session and base model setup
├── models/          # SQLAlchemy Database models
└── schemas/         # Pydantic validation schemas
```

## Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL (optional, defaults to SQLite)

### Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Project

Run the development server using:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.
You can access the interactive Swagger documentation at `http://localhost:8000/docs`.

## API Usage Examples

### 1. Create a Cloud Resource
**POST `/api/v1/resources/`**
```json
{
  "name": "AWS-EC2-Production",
  "service_type": "EC2",
  "unit_price": 0.05
}
```

### 2. Record Usage
**POST `/api/v1/usage/`**
```json
{
  "resource_id": 1,
  "hours": 24.5
}
```

### 3. Get Cost Analytics
**GET `/api/v1/analytics/top-expensive`**
