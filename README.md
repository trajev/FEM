# Family Expense Manager (FEM)

A backend API for managing shared household expenses among family members. Built with FastAPI, async SQLAlchemy, and PostgreSQL.

## What It Does

Family Expense Manager allows members of a household to record, manage, and analyze their shared expenses. One member logs groceries, another logs electricity bills, and all authorized household members can view the shared expense history and understand spending patterns.

## Tech Stack

| Layer          | Technology              |
|----------------|-------------------------|
| Framework      | FastAPI                 |
| Language       | Python 3.10+            |
| ORM            | SQLAlchemy 2.x (async)  |
| Database       | PostgreSQL              |
| DB Driver      | asyncpg                 |
| Migrations     | Alembic                 |
| Validation     | Pydantic v2             |
| Configuration  | pydantic-settings + .env|
| Server         | Uvicorn                 |

## Project Structure

```
FEM/
├── app/
│   ├── main.py                  # FastAPI application entry point
│   ├── core/
│   │   └── config.py            # Settings via pydantic-settings
│   ├── db/
│   │   ├── base.py              # SQLAlchemy DeclarativeBase
│   │   └── connection.py        # Async engine, session factory, get_db dependency
│   ├── models/
│   │   └── user.py              # User SQLAlchemy model
│   ├── schemas/
│   │   └── user.py              # Pydantic request/response schemas
│   ├── routers/
│   │   └── user.py              # User API endpoints
│   ├── service/
│   │   └── user_service.py      # User business logic
│   └── repository/
│       └── user_repository.py   # User database operations
├── alembic/                     # Database migration scripts
├── alembic.ini                  # Alembic configuration
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables (not committed)
└── .gitignore
```

## Architecture

The application follows a three-layer separation pattern:

```
HTTP Request
    └── Router        (handles HTTP concerns, status codes, dependencies)
        └── Service   (business logic, validation rules)
            └── Repository   (database queries, persistence)
                └── AsyncSession → PostgreSQL
```

- **Router** receives requests, injects dependencies via `Depends()`, and returns responses.
- **Service** enforces business rules (e.g., duplicate email check, 404 on missing user).
- **Repository** executes database operations using `flush()` (not `commit()`), allowing the session dependency to manage transaction boundaries via the unit-of-work pattern.

## Current API Endpoints

### Users

| Method | Endpoint         | Description             | Status Code |
|--------|------------------|-------------------------|-------------|
| GET    | `/users/`        | List all users          | 200         |
| POST   | `/users/`        | Create a new user       | 201         |
| GET    | `/users/{user_id}` | Get a user by ID      | 200         |

**Request body for POST `/users/`:**
```json
{
  "name": "string (1-50 chars, required)",
  "email": "valid email address (required)"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com"
}
```

**Error responses:**
- `404` — User not found (GET by ID)
- `409` — Email already exists (POST)
- `422` — Validation error (invalid email, empty name, etc.)

## Setup

### Prerequisites

- Python 3.10+
- PostgreSQL running locally or remotely

### Installation

1. Clone the repository and navigate to the project:
   ```bash
   cd FEM
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv

   # Windows
   .venv\Scripts\activate

   # macOS/Linux
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root:
   ```env
   DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/femdb
   DEBUG=True
   PORT=8000
   ```

5. Create the database:
   ```bash
   createdb femdb
   ```

6. Run Alembic migrations:
   ```bash
   alembic upgrade head
   ```

7. Start the development server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

8. Open the interactive API docs at [http://localhost:8000/docs](http://localhost:8000/docs).

## Environment Variables

| Variable       | Required | Default | Description                         |
|----------------|----------|---------|-------------------------------------|
| `DATABASE_URL` | Yes      | —       | PostgreSQL async connection string  |
| `DEBUG`        | No       | `False` | Enable SQLAlchemy query logging     |
| `PORT`         | No       | `8000`  | Server port                         |

## V1 Roadmap

- [x] Users — Registration and profile CRUD
- [ ] Households — Create a household, get HouseID
- [ ] Join household — Family members join via HouseID
- [ ] Categories — Shared expense categories (Groceries, Rent, etc.)
- [ ] Payment methods — Cash, UPI, Card, etc.
- [ ] Expenses — All members log daily expenses
- [ ] Filtering and pagination — Date range, category, member filters
- [ ] Reports — Daily, weekly, and monthly summaries with breakdowns
- [ ] Authentication — JWT-based register/login
- [ ] Authorization — Household-scoped access control
- [ ] Notification system — Scheduled reminders to add expenses
- [ ] React dashboard — Frontend with forms, filters, and charts
