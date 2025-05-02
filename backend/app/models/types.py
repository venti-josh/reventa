"""Type helpers for SQLAlchemy ORM models."""

from typing import Any, TypeVar, Union

# Create a type alias for Mapped that works with older SQLAlchemy versions
T = TypeVar("T")
Mapped = Union[T, Any]  # noqa: UP007 - Using Union for compatibility alias
