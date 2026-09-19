# PulseWatch — Uptime Monitoring Dashboard (v1 Baseline)

A full-stack, real-time website and API health monitoring dashboard built with **Next.js**, **FastAPI**, **Supabase PostgreSQL**, and **Alembic**.

---

## Architecture Overview

PulseWatch tracks website and API uptime through automated periodic pinging and on-demand health probes, recording latency, HTTP status codes, error logs, and automated incident state transitions.

```
+---------------------------------+          HTTP / REST API          +----------------------------------+
|        Next.js Frontend         | <-------------------------------> |         FastAPI Backend          |
| (TypeScript, Tailwind, App Dir) |     Authorization: Bearer JWT     |  (Python 3.12, Async SQLAlchemy) |
+---------------------------------+                                   +----------------------------------+
                                                                                       |
                                                                             PostgreSQL Connection
                                                                          (postgresql+asyncpg://...)
                                                                                       v
                                                                      +----------------------------------+
                                                                      |       Supabase PostgreSQL        |
                                                                      | (users, monitors, health_checks, |
                                                                      |            incidents)            |
                                                                      +----------------------------------+
```

---

## Tech Stack

### Frontend
- **Framework**: Next.js (App Router, React 18)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Icons**: Lucide React

### Backend
- **Framework**: Python 3.12, FastAPI
- **Database ORM**: Async SQLAlchemy 2.0
- **Database Driver**: `asyncpg` (Application) & `psycopg2-binary` (Alembic)
- **Migrations**: Alembic
- **Authentication**: JWT (JSON Web Tokens) with `passlib` & `bcrypt` password hashing
- **HTTP Client**: `httpx` (Async ping engine)
- **Scheduler**: Async background task worker loop
- **Testing**: `pytest` & `pytest-asyncio`

### Database
- **Database**: Supabase PostgreSQL

---

## Core Features

1. **Authentication**: User registration, login, JWT token authentication, bcrypt password hashing, and user-isolated routes.
2. **Monitor Management**: Create, list, retrieve, update, delete, and enable/disable monitors (with configurable check intervals and timeouts).
3. **Health Checks**: Async HTTP probes measuring latency in ms, HTTP status codes, network errors, and timestamped health logs.
4. **Automated Incident Tracking**:
   - **UP → DOWN**: Creates an active Incident with error details.
   - **DOWN → UP**: Resolves the active Incident with resolution timestamp.
5. **Dashboard & Analytics**: Overall uptime %, total monitors, UP/DOWN count, search/filtering, latency trend chart, and check history.
6. **Alembic Migrations**: Fully versioned database schema migration pipeline.

---

## Project Structure

```
UpTime Monitoring Dashboard/
├── README.md
├── .gitignore
├── backend/
│   ├── .env.example
│   ├── requirements.txt
│   ├── pytest.ini
│   ├── alembic.ini
│   ├── alembic/
│   │   ├── env.py
│   │   └── versions/
│   │       └── 001_initial_schema.py
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── api/          # FastAPI routers (auth, monitors, health_checks, dashboard)
│   │   ├── auth/         # JWT generation, bcrypt password hashing, dependencies
│   │   ├── database/     # Async SQLAlchemy engine & session generator
│   │   ├── models/       # ORM Models (User, Monitor, HealthCheck, Incident)
│   │   ├── schemas/      # Pydantic v2 schemas
│   │   ├── repositories/ # Isolated database query layer
│   │   ├── services/     # Business logic (Auth, Monitor, Checker, Scheduler)
│   │   └── utils/        # Logger utility
│   └── tests/            # Pytest test suite
└── frontend/
    ├── .env.example
    ├── package.json
    ├── tsconfig.json
    ├── tailwind.config.js
    ├── app/              # Next.js App Router pages (login, register, dashboard)
    ├── components/       # UI components (Navbar, StatCard, MonitorList, Charts)
    ├── lib/              # API fetch client & Auth storage helpers
    └── types/            # TypeScript interfaces
```

---

## Environment Configuration

### 1. Backend Configuration (`backend/.env`)

Copy `backend/.env.example` to `backend/.env`:

```bash
# Connection string for Supabase PostgreSQL:
DATABASE_URL=postgresql+asyncpg://postgres:your_db_password@db.your_project.supabase.co:5432/postgres

# Application Security
SECRET_KEY=replace_with_a_secure_random_string_at_least_32_chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# CORS Allowed Origins
CORS_ORIGINS=["http://localhost:3000"]
```

### 2. Frontend Configuration (`frontend/.env.local`)

Copy `frontend/.env.example` to `frontend/.env.local`:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

---

## Local Setup & Quickstart

### Prerequisites
- Python 3.12+
- Node.js 18+ and npm
- Supabase PostgreSQL Database (or any standard PostgreSQL instance)

### Step 1: Set up Supabase PostgreSQL Database & Run Migrations

1. Obtain your PostgreSQL connection URI from your Supabase project settings (*Database -> Connection string -> URI*).
2. Set `DATABASE_URL` in `backend/.env`.
3. Run Alembic database migrations:

```bash
cd backend
python -m pip install -r requirements.txt
alembic upgrade head
```

### Step 2: Start Backend (FastAPI)

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```
- API Swagger Documentation: `http://localhost:8000/api/v1/docs`

### Step 3: Start Frontend (Next.js)

```bash
cd frontend
npm install
npm run dev
```
- Application Web UI: `http://localhost:3000`

---

## Testing

Run automated backend unit and integration tests:

```bash
cd backend
python -m pytest
```

---

## API Endpoints Overview

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/v1/auth/register` | Register a new user account |
| `POST` | `/api/v1/auth/login` | Log in and receive JWT token |
| `GET` | `/api/v1/auth/me` | Get current authenticated user profile |
| `GET` | `/api/v1/monitors` | List all monitors for current user |
| `POST` | `/api/v1/monitors` | Create a new monitor |
| `GET` | `/api/v1/monitors/{id}` | Get single monitor detail (stats, checks, incidents) |
| `PUT` | `/api/v1/monitors/{id}` | Update monitor configuration |
| `DELETE` | `/api/v1/monitors/{id}` | Delete a monitor |
| `PATCH` | `/api/v1/monitors/{id}/toggle` | Pause or resume monitor |
| `POST` | `/api/v1/monitors/{id}/check` | Trigger manual health check probe now |
| `GET` | `/api/v1/health-checks/monitors/{id}` | List recent health check history for a monitor |
| `GET` | `/api/v1/dashboard/summary` | Get aggregated dashboard summary metrics |

---

## Limitations (Baseline v1)

- Notifications (Email, Slack, SMS alerts) are out of scope for v1.
- Advanced multi-region probing nodes will be introduced in future iterations.
- DevOps infrastructure (Docker, Terraform, Ansible, CI/CD, AWS) will be added manually in subsequent project phases.

## Development
Feature development happens on the develop branch.