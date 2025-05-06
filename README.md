# Reventa Project

This repository contains the codebase for the Reventa application.

## Backend (FastAPI)

The backend is a FastAPI application located in the `backend/` directory.

### Structure

```
backend/
├── app/
│   ├── core/         # Core settings, security utilities (config.py, security.py)
│   ├── crud/         # CRUD operations for database models (base.py, user.py)
│   ├── db/           # Database session, base model (base.py, session.py)
│   ├── models/       # SQLAlchemy ORM models (user.py)
│   ├── routers/      # FastAPI routers/endpoints (user_router.py)
│   ├── schemas/      # Pydantic schemas for data validation and serialization (user.py)
│   └── __init__.py
├── alembic/          # Alembic migration scripts
├── alembic.ini       # Alembic configuration
├── .env              # Environment variables (created from .env.example)
├── .env.example      # Example environment variables
├── main.py           # Application entry point
├── requirements.txt  # Project runtime dependencies for pip
├── requirements-dev.txt # Project development dependencies
└── pyproject.toml    # Tool configuration (e.g., Ruff, Mypy)
```

### Setup

1.  **Navigate to backend:**
    ```bash
    cd backend
    ```
2.  **(Optional) Setup Python using pyenv:**
    ```bash
    # Install pyenv if you haven't already
    # MacOS
    brew install pyenv pyenv-virtualenv
    # Linux
    curl https://pyenv.run | bash

    # Install the specified Python version (see .python-version)
    pyenv install $(cat .python-version)

    # Create and activate a virtual environment
    pyenv virtualenv $(cat .python-version) reventa-backend
    pyenv local reventa-backend # This might activate automatically
    # If not automatic: pyenv activate reventa-backend
    ```
    *Alternatively, use your preferred Python environment management (e.g., venv):*
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Install development dependencies:**
    ```bash
    pip install -r requirements-dev.txt
    ```
5.  **Set up environment variables:**
    Copy `.env.example` to `.env` in the `backend` directory and fill in your database URL and other settings.
    ```bash
    cp .env.example .env
    # Edit .env with your configuration
    ```
    *Example `.env` content:*
    ```
    POSTGRES_SERVER=localhost
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    POSTGRES_DB=fastapi_skeleton
    SECRET_KEY=your-secret-key
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```

6.  **Run database migrations:**
    ```bash
    alembic upgrade head
    ```
7.  **Run the development server:**
    ```bash
    uvicorn main:app --reload # Runs the app defined in backend/main.py
    ```

The API documentation (Swagger UI) will be available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

### API Endpoints

The API is organized under the `/api/v1` prefix with the following endpoints:

#### Authentication

- `POST /api/v1/auth/token` - Login to get JWT access token
- `POST /api/v1/auth/register` - Register a new user
- `GET /api/v1/auth/me` - Get current authenticated user information

#### Events

- `GET /api/v1/events/` - List all events (can filter by organization ID)
- `POST /api/v1/events/` - Create a new event
- `GET /api/v1/events/{id}` - Get event details by ID
- `PATCH /api/v1/events/{id}` - Update an event
- `DELETE /api/v1/events/{id}` - Delete an event
- `POST /api/v1/events/{id}/surveys/{survey_id}/launch` - Launch a survey for an event

#### Surveys

- `GET /api/v1/surveys/` - List all surveys
- `POST /api/v1/surveys/` - Create a new survey
- `GET /api/v1/surveys/{id}` - Get survey details by ID
- `PATCH /api/v1/surveys/{id}` - Update a survey (if not published)
- `POST /api/v1/surveys/{id}/publish` - Publish a survey (marking it as unchangeable)

#### Survey Instances

- `GET /api/v1/survey-instances/` - List all survey instances
- `GET /api/v1/survey-instances/{id}` - Get survey instance details

#### Organization Domains

- `GET /api/v1/org/domains/` - List organization domains
- `POST /api/v1/org/domains/` - Add a domain to an organization

#### Public Links

- `GET /api/v1/l/{uuid}` - Get public survey form by link UUID
- `POST /api/v1/l/{uuid}/submit` - Submit a response to a survey

#### Statistics

- `GET /api/v1/events/{id}/stats` - Get statistics for an event
- `GET /api/v1/surveys/{id}/responses/export` - Export survey responses as CSV

### Development Notes

- The application uses FastAPI with async SQLAlchemy.
- Database migrations are handled by Alembic.
- Authentication is implemented using JWT tokens.
- Password hashing is done using bcrypt.
- Linting and formatting are handled by Ruff (configured in `pyproject.toml`).
- Type checking is done by Mypy (configured in `pyproject.toml` and `setup.cfg`).
- Pre-commit hooks are configured in `.pre-commit-config.yaml`.

### Running Tests

(Add instructions for running tests once they are set up)

## Frontend

(Add details about the frontend if applicable)

## Docker Setup (Backend)

This section describes how to run the backend API and PostgreSQL database using Docker and Docker Compose.

### Prerequisites

- Docker: [Install Docker](https://docs.docker.com/get-docker/)
- Docker Compose: Usually included with Docker Desktop.

### Setup

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```
2.  **Create Environment File:**
    Copy the example environment file and customize it if necessary. The `docker-compose.yml` file is configured to read this `.env` file.
    ```bash
    cp .env.example .env
    ```
    *Note:* The default values in `docker-compose.yml` and `Dockerfile` should work for local development (user: `postgres`, password: `postgres`, db: `fastapi_skeleton`, host: `postgres`). You mainly need to ensure `SECRET_KEY` is set in the `.env` file for security.

### Running the Services

1.  **Build and Start Containers:**
    This command builds the API image (if it doesn't exist or `Dockerfile` changed) and starts both the API and PostgreSQL containers in detached mode (`-d`).
    ```bash
    docker-compose up --build -d
    ```
2.  **Check Container Status:**
    ```bash
    docker-compose ps
    ```
    You should see both `fastapi_api` and `fastapi_postgres` running.

3.  **Apply Database Migrations:**
    The API service needs the database schema to be set up. Run the Alembic migrations inside the running API container:
    ```bash
    docker-compose exec api alembic upgrade head
    ```

4.  **Access the API:**
    The API should now be running and accessible:
    - **API Root:** [http://localhost:8000/](http://localhost:8000/)
    - **Swagger Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)

### Development Workflow

- **Hot Reloading:** The `docker-compose.yml` is configured to mount the local `backend` directory into the `/app` directory in the `api` container. The `uvicorn` command also uses the `--reload` flag. This means changes you make to the Python code locally should automatically trigger the server to restart within the container.
- **Viewing Logs:**
    ```bash
    docker-compose logs -f api # Follow API logs
    docker-compose logs -f postgres # Follow PostgreSQL logs
    ```
- **Stopping Services:**
    To stop the containers:
    ```bash
    docker-compose down
    ```
    Add `-v` to also remove the named volume (`postgres_data`) containing the database data:
    ```bash
    docker-compose down -v
    ```

### Database Access

- **Connect via `psql`:** You can connect to the PostgreSQL database running inside the container.
    ```bash
    docker-compose exec postgres psql -U postgres -d fastapi_skeleton
    ```
    (The default user and db name are used here; adjust if you changed them in `.env`).
- **Data Persistence:** The `postgres_data` volume ensures your database data persists even if you stop and remove the containers (unless you use `docker-compose down -v`).
