import uuid
from typing import TYPE_CHECKING

from sqlalchemy import TIMESTAMP, Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.types import Mapped

if TYPE_CHECKING:
    from .organization import Organization
    from .survey_instance import SurveyInstance


class Event(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    start_dt = Column(TIMESTAMP(timezone=True), nullable=False)
    end_dt = Column(TIMESTAMP(timezone=True), nullable=False)
    status = Column(String, nullable=False)

    # Relationships
    organization: Mapped["Organization"] = relationship(
        "Organization", back_populates="events"
    )
    survey_instances: Mapped[list["SurveyInstance"]] = relationship(
        "SurveyInstance", back_populates="event", cascade="all, delete-orphan"
    )
