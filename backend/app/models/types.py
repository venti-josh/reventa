"""Type helpers for SQLAlchemy ORM models."""

from typing import TypeVar, Annotated, Any
from sqlalchemy.orm import mapped_column, relationship

# Import the proper Mapped type directly from SQLAlchemy
from sqlalchemy.orm import Mapped as SQLAMapped

T = TypeVar("T")
# Use the real SQLAlchemy Mapped type
Mapped = SQLAMapped
