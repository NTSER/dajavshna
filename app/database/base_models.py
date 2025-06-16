from typing import Optional
from uuid import UUID

from pydantic import EmailStr
from sqlmodel import SQLModel


class UserBase(SQLModel):
    id: UUID
    name: str
    surname: str
    username: str
    email: EmailStr
    email_verified: bool
    phone_number: str
    password_hash: str


class ImageBase(SQLModel):
    id: UUID
    path: str


class ProductBase(SQLModel):
    id: UUID
    name: str
    price: float
    available: bool
    image_id: Optional[UUID]
    venue_id: UUID


class VenueBase(SQLModel):
    id: UUID
    name: str
    location: str
    available: bool
    image_id: Optional[UUID]
    seller_id: UUID
