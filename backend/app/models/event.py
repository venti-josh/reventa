import enum
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
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
    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    org_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey(Organization.id))
    name: Mapped[str]
    description: Mapped[str | None]
    start_dt: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP(timezone=True))
    end_dt: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP(timezone=True))
    status: Mapped[EventStatus]

    # Relationships
    organization: Mapped[Organization] = relationship(Organization, back_populates="events")
    # Must use string reference to avoid circular import with SurveyInstance
    survey_instances: Mapped[list["SurveyInstance"]] = relationship(
        "SurveyInstance", back_populates="event", cascade="all, delete-orphan"
    )
