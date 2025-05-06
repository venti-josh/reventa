"""Type helpers for SQLAlchemy ORM models."""

from typing import TypeVar

# Import the proper Mapped type directly from SQLAlchemy
from sqlalchemy.orm import Mapped as SQLAMapped

T = TypeVar("T")
# Use the real SQLAlchemy Mapped type
Mapped = SQLAMapped
