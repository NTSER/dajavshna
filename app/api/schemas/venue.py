from typing import Optional
from uuid import UUID

from pydantic import BaseModel
from sqlmodel import Field


class VenuePublic(BaseModel):
    name: str = Field(default=None)
    location: str = Field(default=None)
    available: bool = Field(default=None)
    image_id: Optional[UUID] = Field(default=None)
    id: UUID = Field(default=None)


class VenueCreate(BaseModel):
    name: str
    location: str
    available: bool = Field(default=False)
    image_id: Optional[UUID] = Field(default=None)


class VenueUpdate(BaseModel):
    name: Optional[str] = Field(default=None)
    location: Optional[str] = Field(default=None)
    available: bool = Field(default=False)
    image_id: Optional[UUID] = Field(default=None)
