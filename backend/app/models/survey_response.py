import uuid
from typing import TYPE_CHECKING

from sqlalchemy import TIMESTAMP, Column, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base
from app.models.types import Mapped

if TYPE_CHECKING:
    from .organization import Organization
    from .survey_instance import SurveyInstance


class SurveyResponse(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    survey_instance_id = Column(
        UUID(as_uuid=True), ForeignKey("survey_instances.id"), nullable=False
    )
    email_hash = Column(String, nullable=True)
    answers = Column(JSONB, nullable=False)
    score = Column(Numeric, nullable=True)
    submitted_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    # Relationships
    organization: Mapped["Organization"] = relationship(
        "Organization", back_populates="survey_responses"
    )
    survey_instance: Mapped["SurveyInstance"] = relationship(
        "SurveyInstance", back_populates="survey_responses"
    )
