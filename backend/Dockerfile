# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables to prevent Python from writing pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies if any (e.g., for psycopg2 if it were used instead of asyncpg)
# RUN apt-get update && apt-get install -y --no-install-recommends some-package && rm -rf /var/lib/apt/lists/*

# Install Poetry (if using pyproject.toml for dependencies)
# RUN pip install poetry
# COPY pyproject.toml poetry.lock* ./
# RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi

# Install pip requirements
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Make port 8000 available to the world outside this container
ENV PORT=${PORT:-8000}
EXPOSE ${PORT}

# Define environment variables (can be overridden by docker-compose)
ENV DATABASE_URL=postgresql+asyncpg://postgres:postgres@postgres/reventa
# Change this in production!
ENV SECRET_KEY=your_secret_key_here
ENV ACCESS_TOKEN_EXPIRE_MINUTES=30
ENV POSTGRES_SERVER=postgres
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_DB=reventa
ENV ENVIRONMENT=development

# Run the application using uvicorn
# Add --reload for development to auto-reload on code changes
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "main:app",  "--bind", "0.0.0.0:${PORT}", "--workers", "2", "--timeout", "120"]