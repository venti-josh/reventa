import uuid
from enum import Enum as PyEnum
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import TIMESTAMP, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column

from app.db.base_class import Base
from app.models.types import Mapped
from app.models.organization import Organization
from app.models.event import Event
from app.models.survey import Survey

if TYPE_CHECKING:
    from .link import Link
    from .survey_response import SurveyResponse


class EmailRequirement(PyEnum):
    NONE = "none"
    OPTIONAL_ANY = "optional_any"
    OPTIONAL_ORG = "optional_org"


class SurveyInstance(Base):
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey(Organization.id), nullable=False)
    event_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey(Event.id), nullable=False)
    survey_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey(Survey.id), nullable=False)
    email_requirement: Mapped[EmailRequirement] = mapped_column(
        Enum(EmailRequirement), nullable=False, default=EmailRequirement.NONE
    )
    launched_at: Mapped[Optional[TIMESTAMP]] = mapped_column(TIMESTAMP(timezone=True), nullable=True)

    # Relationships
    organization: Mapped[Organization] = relationship(
        Organization, back_populates="survey_instances"
    )
    event: Mapped[Event] = relationship(Event, back_populates="survey_instances")
    survey: Mapped[Survey] = relationship(Survey, back_populates="survey_instances")
    
    # Must use string references to avoid circular imports
    links: Mapped[List["Link"]] = relationship(
        "Link", back_populates="survey_instance", cascade="all, delete-orphan"
    )
    survey_responses: Mapped[List["SurveyResponse"]] = relationship(
        "SurveyResponse", back_populates="survey_instance", cascade="all, delete-orphan"
    )
