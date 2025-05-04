import enum
import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import TIMESTAMP, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column

from app.db.base_class import Base
from app.models.types import Mapped
from app.models.organization import Organization

if TYPE_CHECKING:
    from .survey_instance import SurveyInstance


class EventStatus(str, enum.Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Event(Base):
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey(Organization.id), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String)
    start_dt: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    end_dt: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    status: Mapped[EventStatus] = mapped_column(Enum(EventStatus), nullable=False)

    # Relationships
    organization: Mapped[Organization] = relationship(
        Organization, back_populates="events"
    )
    # Must use string reference to avoid circular import with SurveyInstance
    survey_instances: Mapped[List["SurveyInstance"]] = relationship(
        "SurveyInstance", back_populates="event", cascade="all, delete-orphan"
    )
