from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import user_router

app = FastAPI(
    title="FastAPI Skeleton",
    description="A skeleton FastAPI application with basic user management",
    version="1.0.0",
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user_router.router, prefix="/api/v1/users", tags=["users"])


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Welcome to FastAPI Skeleton API"}
