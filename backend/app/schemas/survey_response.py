from datetime import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID

from pydantic import BaseModel


class SurveyResponseBase(BaseModel):
    org_id: UUID
    survey_instance_id: UUID
    email_hash: str | None = None
    answers: dict[str, Any]
    score: Decimal | None = None


class SurveyResponseCreate(SurveyResponseBase):
    pass


class SurveyResponseUpdate(BaseModel):
    org_id: UUID | None = None
    survey_instance_id: UUID | None = None
    email_hash: str | None = None
    answers: dict[str, Any] | None = None
    score: Decimal | None = None


class SurveyResponseRead(SurveyResponseBase):
    id: UUID
    submitted_at: datetime

    model_config = {"from_attributes": True}
