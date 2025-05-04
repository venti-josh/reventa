import uuid
from typing import TYPE_CHECKING, Optional
from decimal import Decimal

from sqlalchemy import TIMESTAMP, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import func

from app.db.base_class import Base
from app.models.types import Mapped
from app.models.organization import Organization
from app.models.survey_instance import SurveyInstance

if TYPE_CHECKING:
    from .organization import Organization
    from .survey_instance import SurveyInstance


class SurveyResponse(Base):
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey(Organization.id), nullable=False)
    survey_instance_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey(SurveyInstance.id), nullable=False
    )
    email_hash: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    answers: Mapped[dict] = mapped_column(JSONB, nullable=False)
    score: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    submitted_at: Mapped[Optional[TIMESTAMP]] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())

    # Relationships
    organization: Mapped[Organization] = relationship(
        Organization, back_populates="survey_responses"
    )
    survey_instance: Mapped[SurveyInstance] = relationship(
        SurveyInstance, back_populates="survey_responses"
    )
