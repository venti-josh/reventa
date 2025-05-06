import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.models.organization import Organization

if TYPE_CHECKING:
    from .organization import Organization


class OrgAllowedDomain(Base):
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey(Organization.id), nullable=False)
    domain: Mapped[str] = mapped_column(String, nullable=False)

    # Relationship
    organization: Mapped[Organization] = relationship(Organization, back_populates="allowed_domains")
