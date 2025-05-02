import uuid
from typing import TYPE_CHECKING

from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base
from app.models.types import Mapped

if TYPE_CHECKING:
    from .organization import Organization
    from .survey_instance import SurveyInstance


class Survey(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    title = Column(String, nullable=False)
    schema = Column(JSONB, nullable=False)
    is_published = Column(Boolean, default=False, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    # Relationships
    organization: Mapped["Organization"] = relationship(
        "Organization", back_populates="surveys"
    )
    survey_instances: Mapped[list["SurveyInstance"]] = relationship(
        "SurveyInstance", back_populates="survey", cascade="all, delete-orphan"
    )
