import uuid
from enum import Enum as PyEnum
from typing import TYPE_CHECKING

from sqlalchemy import TIMESTAMP, Column, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.types import Mapped

if TYPE_CHECKING:
    from .event import Event
    from .link import Link
    from .organization import Organization
    from .survey import Survey
    from .survey_response import SurveyResponse


class EmailRequirement(PyEnum):
    NONE = "none"
    OPTIONAL_ANY = "optional_any"
    OPTIONAL_ORG = "optional_org"


class SurveyInstance(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"), nullable=False)
    survey_id = Column(UUID(as_uuid=True), ForeignKey("surveys.id"), nullable=False)
    email_requirement = Column(
        Enum(EmailRequirement), nullable=False, default=EmailRequirement.NONE
    )
    launched_at = Column(TIMESTAMP(timezone=True), nullable=True)

    # Relationships
    organization: Mapped["Organization"] = relationship(
        "Organization", back_populates="survey_instances"
    )
    event: Mapped["Event"] = relationship("Event", back_populates="survey_instances")
    survey: Mapped["Survey"] = relationship("Survey", back_populates="survey_instances")
    links: Mapped[list["Link"]] = relationship(
        "Link", back_populates="survey_instance", cascade="all, delete-orphan"
    )
    survey_responses: Mapped[list["SurveyResponse"]] = relationship(
        "SurveyResponse", back_populates="survey_instance", cascade="all, delete-orphan"
    )
