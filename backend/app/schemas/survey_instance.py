from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.models.survey_instance import EmailRequirement


class SurveyInstanceBase(BaseModel):
    org_id: UUID
    event_id: UUID
    survey_id: UUID
    email_requirement: EmailRequirement = EmailRequirement.NONE
    launched_at: datetime | None = None


class SurveyInstanceCreate(SurveyInstanceBase):
    pass


class SurveyInstanceUpdate(BaseModel):
    org_id: UUID | None = None
    event_id: UUID | None = None
    survey_id: UUID | None = None
    email_requirement: EmailRequirement | None = None
    launched_at: datetime | None = None


class SurveyInstanceRead(SurveyInstanceBase):
    id: UUID

    model_config = {"from_attributes": True}
