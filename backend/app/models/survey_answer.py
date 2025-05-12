import uuid
from typing import TYPE_CHECKING

from sqlalchemy import TIMESTAMP, Boolean, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base_class import Base

if TYPE_CHECKING:
    from .survey_response import SurveyResponse


class SurveyAnswer(Base):
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    response_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("surveyresponse.id"), nullable=False)
    question_idx: Mapped[int] = mapped_column(Integer, nullable=False)
    question_text: Mapped[str] = mapped_column(String, nullable=False)
    is_followup: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    answer: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())

    # Relationships
    response: Mapped["SurveyResponse"] = relationship("SurveyResponse", back_populates="answers")

    # Constraints
    __table_args__ = (
        UniqueConstraint(
            "response_id",
            "question_idx",
            "is_followup",
            name="uq_survey_answer_response_question_followup",
        ),
    )
