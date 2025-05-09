import uuid
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import TIMESTAMP, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base_class import Base
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
    email_hash: Mapped[str | None] = mapped_column(String, nullable=True)
    answers: Mapped[dict] = mapped_column(JSONB, nullable=False)
    score: Mapped[Decimal | None] = mapped_column(Numeric, nullable=True)
    submitted_at: Mapped[TIMESTAMP | None] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())

    # Relationships
    organization: Mapped[Organization] = relationship(Organization, back_populates="survey_responses")
    survey_instance: Mapped[SurveyInstance] = relationship(SurveyInstance, back_populates="survey_responses")
