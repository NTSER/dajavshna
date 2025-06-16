from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr
from sqlmodel import Field


class UserPublic(BaseModel):
    username: str
    id: UUID


class UserCreate(BaseModel):
    username: str
    name: str
    surname: str
    email: EmailStr
    phone_number: str
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    surname: Optional[str] = Field(default=None)
    phone_number: Optional[str] = Field(default=None)
