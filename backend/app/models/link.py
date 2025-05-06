import uuid
from typing import TYPE_CHECKING

from sqlalchemy import TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.models.organization import Organization
from app.models.survey_instance import SurveyInstance

if TYPE_CHECKING:
    from .organization import Organization
    from .survey_instance import SurveyInstance


class Link(Base):
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey(Organization.id), nullable=False)
    survey_instance_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey(SurveyInstance.id), nullable=False
    )
    expires_at: Mapped[TIMESTAMP | None] = mapped_column(TIMESTAMP(timezone=True), nullable=True)

    # Relationships
    organization: Mapped[Organization] = relationship(Organization, back_populates="links")
    survey_instance: Mapped[SurveyInstance] = relationship(SurveyInstance, back_populates="links")
