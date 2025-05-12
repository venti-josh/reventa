from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.survey_answer import SurveyAnswer
from app.schemas.survey_flow import AnswerCreate, AnswerUpdate


class CRUDSurveyAnswer(CRUDBase[SurveyAnswer, AnswerCreate, AnswerUpdate]):
    async def get_by_response_id(self, db: AsyncSession, *, response_id: UUID) -> Sequence[SurveyAnswer]:
        """Get all answers for a specific survey response."""
        result = await db.execute(select(SurveyAnswer).where(SurveyAnswer.response_id == response_id))
        return result.scalars().all()

    async def get_by_response_and_question(
        self, db: AsyncSession, *, response_id: UUID, question_idx: int, is_followup: bool = False
    ) -> SurveyAnswer | None:
        """Get an answer for a specific question in a survey response."""
        result = await db.execute(
            select(SurveyAnswer)
            .where(SurveyAnswer.response_id == response_id)
            .where(SurveyAnswer.question_idx == question_idx)
            .where(SurveyAnswer.is_followup == is_followup)
        )
        return result.scalar_one_or_none()

    async def has_followup(self, db: AsyncSession, *, response_id: UUID, question_idx: int) -> bool:
        """Check if a specific question has a follow-up answer."""
        result = await db.execute(
            select(SurveyAnswer)
            .where(SurveyAnswer.response_id == response_id)
            .where(SurveyAnswer.question_idx == question_idx)
            .where(SurveyAnswer.is_followup == True)
        )
        return result.scalar_one_or_none() is not None


survey_answer_crud = CRUDSurveyAnswer(SurveyAnswer)
