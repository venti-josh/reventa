import uuid
from typing import TYPE_CHECKING

from sqlalchemy import TIMESTAMP, Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
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
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    # Relationships
    allowed_domains: Mapped[list["OrgAllowedDomain"]] = relationship(
        "OrgAllowedDomain", back_populates="organization", cascade="all, delete-orphan"
    )
    users: Mapped[list["User"]] = relationship(
        "User", back_populates="organization", cascade="all, delete-orphan"
    )
    events: Mapped[list["Event"]] = relationship(
        "Event", back_populates="organization", cascade="all, delete-orphan"
    )
    surveys: Mapped[list["Survey"]] = relationship(
        "Survey", back_populates="organization", cascade="all, delete-orphan"
    )
    survey_instances: Mapped[list["SurveyInstance"]] = relationship(
        "SurveyInstance", back_populates="organization", cascade="all, delete-orphan"
    )
    links: Mapped[list["Link"]] = relationship(
        "Link", back_populates="organization", cascade="all, delete-orphan"
    )
    survey_responses: Mapped[list["SurveyResponse"]] = relationship(
        "SurveyResponse", back_populates="organization", cascade="all, delete-orphan"
    )
