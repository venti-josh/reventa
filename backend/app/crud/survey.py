from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.survey import Survey
from app.schemas.survey import SurveyCreate, SurveyUpdate


class CRUDSurvey(CRUDBase[Survey, SurveyCreate, SurveyUpdate]):
    async def get_by_title(self, db: AsyncSession, *, title: str) -> Survey | None:
        result = await db.execute(select(Survey).where(Survey.title == title))
        return result.scalar_one_or_none()

    async def get_by_org_id(self, db: AsyncSession, *, org_id: UUID) -> Sequence[Survey]:
        result = await db.execute(select(Survey).where(Survey.org_id == org_id))
        return result.scalars().all()

    async def get_published(self, db: AsyncSession, *, org_id: UUID) -> Sequence[Survey]:
        result = await db.execute(select(Survey).where(Survey.org_id == org_id).where(Survey.is_published == True))
        return result.scalars().all()


survey_crud = CRUDSurvey(Survey)
