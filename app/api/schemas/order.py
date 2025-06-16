from datetime import datetime
from typing import Optional
from uuid import UUID
from sqlmodel import Field, SQLModel


class OrderItemCreate(SQLModel):
    product_id: UUID
    product_quantity: Optional[int] = Field(default=1)


class OrderBase(SQLModel):
    reservation_time: datetime


class OrderCreate(OrderBase):
    order_items: list[OrderItemCreate]


class OrderPublic(OrderBase):
    pass
