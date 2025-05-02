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

#### Users

- `GET /api/v1/users/` - List users
- `POST /api/v1/users/` - Create user
- `GET /api/v1/users/{user_id}` - Get user by ID
- `PUT /api/v1/users/{user_id}` - Update user
- `DELETE /api/v1/users/{user_id}` - Delete user

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
