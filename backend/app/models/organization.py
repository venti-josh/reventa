import uuid
from typing import TYPE_CHECKING, List

from sqlalchemy import TIMESTAMP, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import func

from app.db.base_class import Base
from app.models.types import Mapped

if TYPE_CHECKING:
    from .event import Event
    from .link import Link
    from .org_allowed_domain import OrgAllowedDomain
    from .survey import Survey
    from .survey_instance import SurveyInstance
    from .survey_response import SurveyResponse
    from .user import User


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())

    # Relationships
    allowed_domains: Mapped[List["OrgAllowedDomain"]] = relationship(
        "OrgAllowedDomain", back_populates="organization", cascade="all, delete-orphan"
    )
    users: Mapped[List["User"]] = relationship(
        "User", back_populates="organization", cascade="all, delete-orphan"
    )
    events: Mapped[List["Event"]] = relationship(
        "Event", back_populates="organization", cascade="all, delete-orphan"
    )
    surveys: Mapped[List["Survey"]] = relationship(
        "Survey", back_populates="organization", cascade="all, delete-orphan"
    )
    survey_instances: Mapped[List["SurveyInstance"]] = relationship(
        "SurveyInstance", back_populates="organization", cascade="all, delete-orphan"
    )
    links: Mapped[List["Link"]] = relationship(
        "Link", back_populates="organization", cascade="all, delete-orphan"
    )
    survey_responses: Mapped[List["SurveyResponse"]] = relationship(
        "SurveyResponse", back_populates="organization", cascade="all, delete-orphan"
    )
