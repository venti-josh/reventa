from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.survey_instance import SurveyInstance
from app.schemas.survey_instance import SurveyInstanceCreate, SurveyInstanceUpdate


class CRUDSurveyInstance(CRUDBase[SurveyInstance, SurveyInstanceCreate, SurveyInstanceUpdate]):
    async def get_by_org_id(self, db: AsyncSession, *, org_id: UUID) -> Sequence[SurveyInstance]:
        result = await db.execute(select(SurveyInstance).where(SurveyInstance.org_id == org_id))
        return result.scalars().all()

    async def get_by_survey_id(self, db: AsyncSession, *, survey_id: UUID) -> Sequence[SurveyInstance]:
        result = await db.execute(select(SurveyInstance).where(SurveyInstance.survey_id == survey_id))
        return result.scalars().all()

    async def get_by_event_id(self, db: AsyncSession, *, event_id: UUID) -> Sequence[SurveyInstance]:
        result = await db.execute(select(SurveyInstance).where(SurveyInstance.event_id == event_id))
        return result.scalars().all()

    async def get_launched(self, db: AsyncSession, *, org_id: UUID) -> Sequence[SurveyInstance]:
        result = await db.execute(
            select(SurveyInstance).where(SurveyInstance.org_id == org_id).where(SurveyInstance.launched_at.isnot(None))
        )
        return result.scalars().all()


survey_instance_crud = CRUDSurveyInstance(SurveyInstance)
