from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.survey_response import SurveyResponse
from app.schemas.survey_response import SurveyResponseCreate, SurveyResponseUpdate


class CRUDSurveyResponse(
    CRUDBase[SurveyResponse, SurveyResponseCreate, SurveyResponseUpdate]
):
    async def get_by_org_id(
        self, db: AsyncSession, *, org_id: UUID
    ) -> list[SurveyResponse]:
        result = await db.execute(
            select(SurveyResponse).where(SurveyResponse.org_id == org_id)
        )
        return result.scalars().all()

    async def get_by_survey_instance_id(
        self, db: AsyncSession, *, survey_instance_id: UUID
    ) -> list[SurveyResponse]:
        result = await db.execute(
            select(SurveyResponse).where(
                SurveyResponse.survey_instance_id == survey_instance_id
            )
        )
        return result.scalars().all()

    async def get_by_email_hash(
        self, db: AsyncSession, *, survey_instance_id: UUID, email_hash: str
    ) -> SurveyResponse | None:
        result = await db.execute(
            select(SurveyResponse)
            .where(SurveyResponse.survey_instance_id == survey_instance_id)
            .where(SurveyResponse.email_hash == email_hash)
        )
        return result.scalar_one_or_none()


survey_response_crud = CRUDSurveyResponse(SurveyResponse)
