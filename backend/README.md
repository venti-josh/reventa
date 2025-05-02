# FastAPI Skeleton

A skeleton FastAPI application with basic user management functionality.

## Project Structure

```
backend/
├── app/
│   ├── core/           # Core functionality
│   │   ├── config.py   # Configuration settings
│   │   └── security.py # Security utilities
│   ├── crud/           # CRUD operations
│   │   ├── base.py     # Base CRUD class
│   │   └── user.py     # User CRUD operations
│   ├── db/             # Database
│   │   ├── base.py     # Base class for models
│   │   └── session.py  # Database session
│   ├── models/         # SQLAlchemy models
│   │   └── user.py     # User model
│   ├── schemas/        # Pydantic schemas
│   │   └── user.py     # User schemas
│   └── routers/        # API routers
│       └── user_router.py # User routes
├── requirements.txt    # Project dependencies
└── main.py            # Application entry point
```

## Setup

1. Setup Python using pyenv:
```bash
# Install pyenv if you haven't already
# MacOS
brew install pyenv pyenv-virtualenv
# Linux
curl https://pyenv.run | bash

# Install the latest Python version
pyenv install 3.12.2

# Create a virtual environment using pyenv-virtualenv
pyenv virtualenv 3.12.2 reventa-backend
pyenv local reventa-backend

# Activate the environment (may happen automatically with pyenv local)
pyenv activate reventa-backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with the following variables:
```
POSTGRES_SERVER=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=fastapi_skeleton
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

4. Start the application:
```bash
uvicorn main:app --reload
```

## API Endpoints

### Users

- `GET /api/v1/users/` - List users
- `POST /api/v1/users/` - Create user
- `GET /api/v1/users/{user_id}` - Get user by ID
- `PUT /api/v1/users/{user_id}` - Update user
- `DELETE /api/v1/users/{user_id}` - Delete user

## Development

- The application uses FastAPI with async SQLAlchemy
- Database migrations are handled by Alembic
- Authentication is implemented using JWT tokens
- Password hashing is done using bcrypt 