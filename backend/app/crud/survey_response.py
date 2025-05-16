from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.survey_response import SurveyResponse
from app.schemas.survey_flow import SurveyResponseCreate, SurveyResponseUpdate


class CRUDSurveyResponse(CRUDBase[SurveyResponse, SurveyResponseCreate, SurveyResponseUpdate]):
    async def get_by_survey_id(self, db: AsyncSession, *, survey_id: UUID) -> Sequence[SurveyResponse]:
        """Get all responses for a specific survey."""
        result = await db.execute(select(SurveyResponse).where(SurveyResponse.survey_id == survey_id))
        return result.scalars().all()

    async def get_active_responses(self, db: AsyncSession) -> Sequence[SurveyResponse]:
        """Get all active (unfinished) survey responses."""
        result = await db.execute(select(SurveyResponse).where(SurveyResponse.finished_at.is_(None)))
        return result.scalars().all()

    async def increment_current_index(self, db: AsyncSession, *, response_id: UUID) -> SurveyResponse:
        """Increment the current index of a survey response."""
        stmt = (
            update(SurveyResponse)
            .where(SurveyResponse.id == response_id)
            .values(current_index=SurveyResponse.current_index + 1)
            .returning(SurveyResponse)
        )
        result = await db.execute(stmt)
        response = result.scalar_one()
        await db.commit()
        return response

    async def mark_finished(self, db: AsyncSession, *, response_id: UUID) -> SurveyResponse:
        """Mark a survey response as finished."""
        from sqlalchemy.sql import func

        stmt = (
            update(SurveyResponse)
            .where(SurveyResponse.id == response_id)
            .values(finished_at=func.now())
            .returning(SurveyResponse)
        )
        result = await db.execute(stmt)
        response = result.scalar_one()
        await db.commit()
        return response

    async def get_by_survey_instance_id(
        self, db: AsyncSession, *, survey_instance_id: UUID
    ) -> Sequence[SurveyResponse]:
        """Get all responses for a specific survey instance."""
        result = await db.execute(select(SurveyResponse).where(SurveyResponse.survey_instance_id == survey_instance_id))
        return result.scalars().all()


survey_response_crud = CRUDSurveyResponse(SurveyResponse)
