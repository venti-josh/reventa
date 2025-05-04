import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import TIMESTAMP, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import func

from app.db.base_class import Base
from app.models.types import Mapped
from app.models.organization import Organization

if TYPE_CHECKING:
    from .organization import Organization


class User(Base):

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey(Organization.id), nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())

    # Relationship
    organization: Mapped[Organization] = relationship(Organization, back_populates="users")
