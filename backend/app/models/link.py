import uuid
from typing import TYPE_CHECKING

from sqlalchemy import TIMESTAMP, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.types import Mapped

if TYPE_CHECKING:
    from .organization import Organization
    from .survey_instance import SurveyInstance


class Link(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    survey_instance_id = Column(
        UUID(as_uuid=True), ForeignKey("survey_instances.id"), nullable=False
    )
    expires_at = Column(TIMESTAMP(timezone=True), nullable=True)

    # Relationships
    organization: Mapped["Organization"] = relationship(
        "Organization", back_populates="links"
    )
    survey_instance: Mapped["SurveyInstance"] = relationship(
        "SurveyInstance", back_populates="links"
    )
