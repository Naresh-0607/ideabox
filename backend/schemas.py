from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class IdeaStatus(str, Enum):
    inbox = "Inbox"
    parked = "Parked"
    active = "Active"
    completed = "Completed"


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    created_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class IdeaCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=10000)
    tags: list[str] = Field(default_factory=list, max_length=20)
    status: IdeaStatus = IdeaStatus.inbox

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Title cannot be blank")
        return value

    @field_validator("tags")
    @classmethod
    def clean_tags(cls, value: list[str]) -> list[str]:
        cleaned = [tag.strip() for tag in value if tag.strip()]
        if any(len(tag) > 40 for tag in cleaned):
            raise ValueError("Tags must be 40 characters or fewer")
        return list(dict.fromkeys(cleaned))


class IdeaUpdate(IdeaCreate):
    pass


class IdeaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    title: str
    description: str | None
    tags: list[str]
    status: IdeaStatus
    created_at: datetime
    updated_at: datetime
