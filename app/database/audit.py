from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy.dialects import postgresql
from sqlmodel import Column, Field
from .base_models import ProductBase, UserBase, VenueBase


class ProductAudit(ProductBase, table=True):
    id: UUID = Field(
        sa_column=Column(postgresql.UUID, primary_key=True, default=uuid4),
    )
    product_id: UUID
    changed_at: datetime = Field(
        sa_column=Column(postgresql.TIMESTAMP, default=datetime.now)
    )
    operation: str


class VenueAudit(VenueBase, table=True):
    id: UUID = Field(
        sa_column=Column(postgresql.UUID, primary_key=True, default=uuid4),
    )
    venue_id: UUID
    changed_at: datetime = Field(
        sa_column=Column(postgresql.TIMESTAMP, default=datetime.now)
    )
    operation: str


class SellerAudit(UserBase, table=True):
    id: UUID = Field(
        sa_column=Column(postgresql.UUID, primary_key=True, default=uuid4),
    )
    seller_id: UUID
    changed_at: datetime = Field(
        sa_column=Column(postgresql.TIMESTAMP, default=datetime.now)
    )
    operation: str


class ConsumerAudit(UserBase, table=True):
    id: UUID = Field(
        sa_column=Column(postgresql.UUID, primary_key=True, default=uuid4),
    )
    consumer_id: UUID
    changed_at: datetime = Field(
        sa_column=Column(postgresql.TIMESTAMP, default=datetime.now)
    )
    operation: str
