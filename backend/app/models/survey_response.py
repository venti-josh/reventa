import uuid
from typing import TYPE_CHECKING

from sqlalchemy import TIMESTAMP, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base_class import Base
from app.models.survey import Survey

if TYPE_CHECKING:
    from .survey import Survey
    from .survey_answer import SurveyAnswer
    from .survey_instance import SurveyInstance


class SurveyResponse(Base):
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    survey_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey(Survey.id), nullable=False)
    survey_instance_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("surveyinstance.id"), nullable=False
    )
    started_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    finished_at: Mapped[TIMESTAMP | None] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    current_index: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    meta: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    # Relationships
    survey: Mapped[Survey] = relationship(Survey, back_populates="survey_responses")
    survey_instance: Mapped["SurveyInstance"] = relationship("SurveyInstance", back_populates="survey_responses")
    answers: Mapped[list["SurveyAnswer"]] = relationship(
        "SurveyAnswer", back_populates="response", cascade="all, delete-orphan"
    )
