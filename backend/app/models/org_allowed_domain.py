import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.types import Mapped

if TYPE_CHECKING:
    from .organization import Organization


class OrgAllowedDomain(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    domain = Column(String, nullable=False)

    # Relationship
    organization: Mapped["Organization"] = relationship(
        "Organization", back_populates="allowed_domains"
    )
