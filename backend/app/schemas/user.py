from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    name: str | None = None


class UserCreate(UserBase):
    password: str
    org_id: UUID


class UserUpdate(UserBase):
    password: str | None = None
    org_id: UUID | None = None


class UserRead(UserBase):
    id: UUID
    org_id: UUID
    created_at: datetime

    model_config = {"from_attributes": True}


class UserInDB(UserRead):
    hashed_password: str
