from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ProductPublic(BaseModel):
    id: Optional[UUID] = Field(default=None)
    name: Optional[str] = Field(default=None)
    price: Optional[float] = Field(default=None)
    available: Optional[bool] = Field(default=None)
    image_id: Optional[UUID] = Field(default=None)


class ProductCreate(BaseModel):
    name: str
    price: float
    available: Optional[bool] = Field(default=None)
    image_id: Optional[UUID] = Field(default=None)


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(default=None)
    price: Optional[float] = Field(default=None)
    available: Optional[bool] = Field(default=None)
    image_id: Optional[UUID] = Field(default=None)
