# 🏡 Family Expense Manager (FEM)

A full-stack application for families and shared households to record everyday expenses, view where their money goes, and understand household spending over time.

The goal of **Family Expense Manager (FEM)** is to give household members one shared place to manage expenses instead of relying on scattered notes, messages, or spreadsheets. A member can create a household, invite other members, record expenses, and review household spending. The application will provide daily, weekly, and monthly summaries, with a React dashboard for viewing the information clearly.

> **Project status:** In development. This README describes the intended scope and planned API. Features and endpoints are not considered implemented until they are available in the application.

---

## 💡 1. Why this project?

Household spending is shared, but expense information is often scattered across different people and places. FEM is intended to help a household:

- Keep household expenses in one shared history.
- Record who paid, what the expense was for, and when it happened.
- Organize spending by category and payment method.
- Filter and paginate expense history instead of loading every record at once.
- Review daily, weekly, and monthly spending summaries.
- Give family members a common view of household finances.

**FEM is an expense-tracking and spending-summary application.** It is not intended to calculate each person's debt or automatically split bills.

---

## 🚀 2. Planned features

### 👤 1. Users and household membership
- Users can register and sign in.
- A user can create a household (for example, a family home).
- The household creator becomes a member of that household.
- Other registered users can join using a household ID and an invitation code or link.
- Each user belongs to one household in FEM.
- Household members can access shared household expense information according to the application's authorization rules.

### 💸 2. Expense management
- Create, view, edit, and delete expenses.
- Record details such as amount, description, expense date, category, payment method, and the member who recorded the expense.
- Associate each expense with a household so its data remains within that household.
- View the household's expense history.

### 🏷️ 3. Categories and payment methods
- Use categories such as groceries, rent, utilities, transport, and healthcare.
- Use payment methods such as cash, debit card, credit card, and UPI.
- Keep categories and payment methods associated with a household so its members share the same options.

### 📜 4. Expense history
- Filter expenses by date range, category, payment method, and member where applicable.
- Support pagination so clients can retrieve results in manageable pages.
- Apply household-level access checks to prevent users from viewing another household's data.

### 📊 5. Spending summaries
- Provide daily, weekly, and monthly expense summaries.
- Show total spending for the selected period.
- Break down spending by category and, where useful, by member.
- Supply summary data for the React dashboard.

### 🖥️ 6. React dashboard
- Connect the React frontend to the FastAPI backend.
- Show household spending summaries and recent expenses.
- Provide screens for managing expenses, categories, and payment methods.
- Provide expense-history filters and pagination.

---

## 🛠️ 3. Planned technology stack

| Area | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend** | React | Dashboard and user interface |
| **Backend** | Python, FastAPI | REST API and application logic |
| **Data validation** | Pydantic v2 | Validate incoming requests and shape API responses |
| **ORM / database access** | SQLAlchemy 2.x (async) | Map Python models to relational data and execute asynchronous database operations |
| **Database** | PostgreSQL | Persist users, households, expenses, and related records |
| **Database driver** | asyncpg | High-performance asynchronous PostgreSQL driver |
| **Database migrations** | Alembic | Track and apply database schema changes |
| **ASGI server** | Uvicorn | Run the FastAPI application |

The stack may be extended as the project requires. Authentication, deployment, and other infrastructure choices will be documented when they are selected and implemented.

---

## 🏛️ 4. Backend architecture

The backend follows a layered structure to keep HTTP handling, business rules, and database access clean and decoupled:

```
                  ┌──────────────────────────────┐
                  │    React Frontend / Client   │
                  └──────────────┬───────────────┘
                                 │ HTTP / JSON
                                 ▼
                  ┌──────────────────────────────┐
                  │         Router Layer         │  <-- app/routers/
                  │  (HTTP parsing, DI, status)  │
                  └──────────────┬───────────────┘
                                 │
                                 ▼
                  ┌──────────────────────────────┐
                  │        Service Layer         │  <-- app/service/
                  │ (Business logic, validation) │
                  └──────────────┬───────────────┘
                                 │
                                 ▼
                  ┌──────────────────────────────┐
                  │       Repository Layer       │  <-- app/repository/
                  │   (SQLAlchemy CRUD queries)  │
                  └──────────────┬───────────────┘
                                 │
                                 ▼
                  ┌──────────────────────────────┐
                  │  Unit of Work / AsyncSession │  <-- app/db/connection.py
                  │  (PostgreSQL Transaction)    │
                  └──────────────┬───────────────┘
                                 │
                                 ▼
                  ┌──────────────────────────────┐
                  │      PostgreSQL Database     │
                  └──────────────────────────────┘
```

- **Routers (`app/routers/`)**: Define endpoints, receive validated input, handle HTTP concerns and status codes, and inject dependencies (`Depends`).
- **Schemas (`app/schemas/`)**: Define Pydantic request and response contracts and perform data validation.
- **Services (`app/service/`)**: Implement core use cases and business rules (e.g., verifying user existence before creating a house, ensuring cross-household data isolation).
- **Repositories (`app/repository/`)**: Encapsulate persistence logic and SQLAlchemy database operations using `session.flush()`.
- **Models (`app/models/`)**: Declarative SQLAlchemy models representing persisted database entities and relationships.
- **Database dependencies (`app/db/connection.py`)**: Provide asynchronous database sessions and manage transaction boundaries (Unit of Work with auto-commit on success and rollback on failure).

This separation keeps the application maintainable, testable, and adaptable as new features are added.

---

## 📁 5. Project directory structure

```
FEM/
├── alembic/                     # Database migration environment and revision scripts
│   ├── versions/                # Generated migration scripts
│   └── env.py                   # Async migration runner and metadata binding
├── alembic.ini                  # Alembic runtime configuration
├── requirements.txt             # Project dependencies and pinned versions
├── .env                         # Local environment secrets (ignored by git)
├── .gitignore                   # Version control ignore rules
└── app/
    ├── main.py                  # Application entry point and router registration
    ├── core/
    │   └── config.py            # Type-safe application settings (pydantic-settings)
    ├── db/
    │   ├── base.py              # DeclarativeBase SQLAlchemy parent
    │   └── connection.py        # Async engine, sessionmaker, and get_db dependency
    ├── models/                  # SQLAlchemy ORM database models
    │   ├── mixins.py            # Common model mixins (e.g. TimestampMixin)
    │   ├── user.py              # User entity
    │   ├── house.py             # House entity
    │   └── house_membership.py  # User-to-House membership junction
    ├── schemas/                 # Pydantic validation and serialization models
    │   ├── user.py              # User request / response schemas
    │   └── house.py             # House request / response schemas
    ├── repository/              # Persistence layer (database interactions)
    │   ├── user_repository.py   # User CRUD queries
    │   └── house_repository.py  # House CRUD queries
    ├── service/                 # Core domain business logic
    │   ├── user_service.py      # User validation and business workflows
    │   └── house_service.py     # House creation and code generation workflows
    ├── routers/                 # API endpoint definitions
    │   ├── user.py              # /users endpoints
    │   └── house.py             # /houses endpoints
    └── utils/                   # Shared utility helpers (e.g., join code generator)
```

---

## 🗄️ 6. Data model and relationships

The central concept is the **household**. Expenses, categories, and payment methods belong to a household, while users are associated with a household through a membership record.

```text
User
 ├── creates ───────────────> Household
 └── has one membership ────> HouseholdMembership
 │
 └── belongs to Household

Household
 ├── has many HouseholdMembership records
 ├── has many Expenses
 ├── has many Categories
 └── has many PaymentMethods

Expense
 ├── belongs to one Household
 ├── recorded by one User
 ├── uses one Category
 └── uses one PaymentMethod
```

### 🧩 Main entities

- **User** — a person's account and login identity.
- **Household** — the shared space for a family or household's expense data. It stores household details and the information needed to invite members.
- **HouseholdMembership** — connects a user to a household and records membership-related information, such as when the user joined and their role if roles are used.
- **Expense** — a household expense, including its amount, description, date, category, payment method, and the user who recorded it.
- **Category** — a household-defined or household-available label used to group expenses.
- **PaymentMethod** — a household-defined or household-available way an expense was paid.

### ⚖️ Important relationship decisions

- FEM allows **one household per user**. The database should enforce this rule on the membership relationship.
- A household can have many members and many expenses.
- A household's categories and payment methods are shared by its members.
- Each expense must reference the household it belongs to. Backend authorization must verify household membership rather than trusting an ID supplied by the client.
- The expense's recorded-by user is different from the household itself: the household owns the shared record, while the user identifies who entered it.
- Family relationship labels such as *father*, *mother*, *son*, or *grandson* are not required for expense tracking. A household membership means that a person belongs to the household; it does not describe their family-tree relationship.

These are domain-level relationships. Exact column names, constraints, delete behavior, and role rules will be finalized in the database models and migrations.

---

## 📡 7. Planned API outline

The backend will expose REST endpoints. The paths below are a **proposed API contract**, not a guarantee that every endpoint already exists. The running FastAPI OpenAPI documentation at `/docs` will be the source of truth for implemented request fields, response schemas, and status codes.

| Area | Method and proposed path | Purpose |
| :--- | :--- | :--- |
| Authentication | `POST /auth/register` | Create a user account |
| Authentication | `POST /auth/login` | Authenticate a user |
| Users | `GET /users/me` | Get the current user's profile |
| Households | `POST /households` | Create a household |
| Households | `GET /households/me` | Get the current user's household |
| Households | `GET /households/{household_id}` | Get household details, subject to membership checks |
| Membership | `POST /households/join` | Join a household using its ID and invitation code |
| Membership | `GET /households/{household_id}/members` | List household members |
| Expenses | `POST /expenses` | Create an expense |
| Expenses | `GET /expenses` | List household expenses with filters and pagination |
| Expenses | `GET /expenses/{expense_id}` | Get one expense |
| Expenses | `PATCH /expenses/{expense_id}` | Update an expense |
| Expenses | `DELETE /expenses/{expense_id}` | Delete an expense |
| Categories | `POST /categories` | Create a category |
| Categories | `GET /categories` | List household categories |
| Categories | `PATCH /categories/{category_id}` | Update a category |
| Categories | `DELETE /categories/{category_id}` | Delete a category, subject to usage rules |
| Payment methods | `POST /payment-methods` | Create a payment method |
| Payment methods | `GET /payment-methods` | List household payment methods |
| Payment methods | `PATCH /payment-methods/{payment_method_id}` | Update a payment method |
| Payment methods | `DELETE /payment-methods/{payment_method_id}` | Delete a payment method, subject to usage rules |
| Summaries | `GET /summaries/daily` | Get daily spending totals and breakdowns |
| Summaries | `GET /summaries/weekly` | Get weekly spending totals and breakdowns |
| Summaries | `GET /summaries/monthly` | Get monthly spending totals and breakdowns |

Endpoint names and grouping may change as implementation progresses. Email reporting is not currently included in the planned functionality.

---

## 📖 8. API documentation

When the backend is running locally:

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`
- **OpenAPI schema:** `http://localhost:8000/openapi.json`

Use `/docs` to inspect and try the endpoints that are actually implemented. The planned API table above is a proposed outline; the generated OpenAPI schema reflects the current application.

---

## 💻 9. Running locally

These are the general steps for the backend. Exact commands may need to be adjusted to match the repository's current configuration.

### 📋 Prerequisites

- Python version supported by the project dependencies (Python 3.10+)
- PostgreSQL
- Git

### ⚙️ Setup

1. **Clone the repository and enter the project directory:**
   ```bash
   git clone <repository-url>
   cd FEM
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # Windows PowerShell
   python -m venv .venv
   .venv\Scripts\Activate.ps1

   # macOS / Linux
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install the project's dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a local `.env` file** using the environment variables required by the application. Keep real credentials out of source control.
   ```env
   DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/femdb
   DEBUG=True
   PORT=8000
   ```

5. **Create the PostgreSQL database** configured for your local environment:
   ```bash
   createdb femdb
   ```

6. **Apply database migrations:**
   ```bash
   alembic upgrade head
   ```

7. **Start the development server:**
   ```bash
   uvicorn app.main:app --reload
   ```

8. **Open the interactive API documentation:**
   Visit `http://localhost:8000/docs` to inspect and test the API.

---

## 🔮 10. Scope and future decisions

The application focuses on household expense tracking and summaries. Authentication details, membership roles, invitation expiry, currency handling, and deployment configuration will be specified as those parts are designed and implemented. Daily and weekly email reports may be considered separately in the future.

---

## 🤝 11. Contributing and feedback

This is a learning and portfolio project built incrementally. Suggestions, bug reports, and feedback are welcome through GitHub Issues.
