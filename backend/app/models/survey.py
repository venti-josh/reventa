import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import TIMESTAMP, Boolean, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import func

from app.db.base_class import Base
from app.models.types import Mapped
from app.models.organization import Organization

if TYPE_CHECKING:
    from .survey_instance import SurveyInstance


class Survey(Base):
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey(Organization.id), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    schema: Mapped[dict] = mapped_column(JSONB, nullable=False)
    is_published: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[Optional[TIMESTAMP]] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())

    # Relationships
    organization: Mapped[Organization] = relationship(
        Organization, back_populates="surveys"
    )
    # Must use string reference to avoid circular import with SurveyInstance
    survey_instances: Mapped[List["SurveyInstance"]] = relationship(
        "SurveyInstance", back_populates="survey", cascade="all, delete-orphan"
    )
