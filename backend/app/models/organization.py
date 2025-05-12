import uuid
from typing import TYPE_CHECKING

from sqlalchemy import TIMESTAMP, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base_class import Base

if TYPE_CHECKING:
    from .event import Event
    from .link import Link
    from .org_allowed_domain import OrgAllowedDomain
    from .survey import Survey
    from .survey_instance import SurveyInstance
    from .user import User


class Organization(Base):
    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())

    # All relationships must use string references because Organization is imported by all other models
    # Using direct class references would create circular imports
    allowed_domains: Mapped[list["OrgAllowedDomain"]] = relationship(
        "OrgAllowedDomain", back_populates="organization", cascade="all, delete-orphan"
    )
    users: Mapped[list["User"]] = relationship("User", back_populates="organization", cascade="all, delete-orphan")
    events: Mapped[list["Event"]] = relationship("Event", back_populates="organization", cascade="all, delete-orphan")
    surveys: Mapped[list["Survey"]] = relationship(
        "Survey", back_populates="organization", cascade="all, delete-orphan"
    )
    survey_instances: Mapped[list["SurveyInstance"]] = relationship(
        "SurveyInstance", back_populates="organization", cascade="all, delete-orphan"
    )
    links: Mapped[list["Link"]] = relationship("Link", back_populates="organization", cascade="all, delete-orphan")
