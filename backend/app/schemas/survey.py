from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel


class SurveyBase(BaseModel):
    title: str
    schema: dict[str, Any]
    is_published: bool = False
    org_id: UUID


class SurveyCreate(SurveyBase):
    pass


class SurveyUpdate(BaseModel):
    title: str | None = None
    schema: dict[str, Any] | None = None
    is_published: bool | None = None
    org_id: UUID | None = None


class SurveyRead(SurveyBase):
    id: UUID
    created_at: datetime

    model_config = {"from_attributes": True}
