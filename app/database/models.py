from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy.dialects import postgresql
from sqlmodel import Column, Field, Relationship, SQLModel
from .base_models import UserBase, ImageBase, ProductBase, VenueBase


class Product(ProductBase, table=True):
    id: UUID = Field(
        sa_column=Column(postgresql.UUID, primary_key=True, default=uuid4),
    )
    created_at: datetime = Field(
        sa_column=Column(postgresql.TIMESTAMP, default=datetime.now)
    )
    image_id: Optional[UUID] = Field(foreign_key="productimage.id", default=None)
    venue_id: UUID = Field(foreign_key="venue.id")
    image: Optional["ProductImage"] = Relationship(
        back_populates="product", sa_relationship_kwargs={"lazy": "selectin"}
    )
    venue: "Venue" = Relationship(
        back_populates="products", sa_relationship_kwargs={"lazy": "selectin"}
    )
    order_items: "OrderItem" = Relationship(
        back_populates="product", sa_relationship_kwargs={"lazy": "selectin"}
    )


class ProductImage(ImageBase, table=True):
    id: UUID = Field(
        sa_column=Column(postgresql.UUID, primary_key=True, default=uuid4),
    )

    product: Product = Relationship(
        back_populates="image", sa_relationship_kwargs={"lazy": "selectin"}
    )
    created_at: datetime = Field(
        sa_column=Column(postgresql.TIMESTAMP, default=datetime.now)
    )


class Venue(VenueBase, table=True):
    id: UUID = Field(
        sa_column=Column(postgresql.UUID, primary_key=True, default=uuid4),
    )
    created_at: datetime = Field(
        sa_column=Column(postgresql.TIMESTAMP, default=datetime.now)
    )
    image_id: Optional[UUID] = Field(foreign_key="venueimage.id", default=None)
    seller_id: UUID = Field(foreign_key="seller.id")
    image: Optional["VenueImage"] = Relationship(
        back_populates="venue", sa_relationship_kwargs={"lazy": "selectin"}
    )
    seller: "Seller" = Relationship(
        back_populates="venues", sa_relationship_kwargs={"lazy": "selectin"}
    )

    products: list[Product] = Relationship(
        back_populates="venue", sa_relationship_kwargs={"lazy": "selectin"}
    )

    orders: list["Order"] = Relationship(
        back_populates="venue", sa_relationship_kwargs={"lazy": "selectin"}
    )


class VenueImage(ImageBase, table=True):
    id: UUID = Field(
        sa_column=Column(postgresql.UUID, primary_key=True, default=uuid4),
    )

    venue: Venue = Relationship(
        back_populates="image", sa_relationship_kwargs={"lazy": "selectin"}
    )
    created_at: datetime = Field(
        sa_column=Column(postgresql.TIMESTAMP, default=datetime.now)
    )


class OrderItem(SQLModel, table=True):
    id: UUID = Field(
        sa_column=Column(postgresql.UUID, primary_key=True, default=uuid4),
    )
    product_id: UUID = Field(foreign_key="product.id")
    product: Product = Relationship(
        back_populates="order_items", sa_relationship_kwargs={"lazy": "selectin"}
    )
    product_quantity: Optional[int] = Field(default=1)

    order_id: UUID = Field(foreign_key="order.id")
    order: "Order" = Relationship(
        back_populates="order_items", sa_relationship_kwargs={"lazy": "selectin"}
    )
    created_at: datetime = Field(
        sa_column=Column(postgresql.TIMESTAMP, default=datetime.now)
    )


class Order(SQLModel, table=True):
    id: UUID = Field(
        sa_column=Column(postgresql.UUID, primary_key=True, default=uuid4),
    )
    reservation_time: datetime

    venue_id: UUID = Field(foreign_key="venue.id")
    venue: Venue = Relationship(
        back_populates="orders", sa_relationship_kwargs={"lazy": "selectin"}
    )

    consumer_id: UUID = Field(foreign_key="consumer.id")
    consumer: "Consumer" = Relationship(
        back_populates="orders", sa_relationship_kwargs={"lazy": "selectin"}
    )
    order_items: list[OrderItem] = Relationship(
        back_populates="order", sa_relationship_kwargs={"lazy": "selectin"}
    )
    review: "Review" = Relationship(
        back_populates="order", sa_relationship_kwargs={"lazy": "selectin"}
    )
    created_at: datetime = Field(
        sa_column=Column(postgresql.TIMESTAMP, default=datetime.now)
    )


class Seller(UserBase, table=True):
    id: UUID = Field(
        sa_column=Column(postgresql.UUID, primary_key=True, default=uuid4),
    )
    email_verified: bool = Field(default=True)
    venues: list[Venue] = Relationship(
        back_populates="seller", sa_relationship_kwargs={"lazy": "selectin"}
    )
    created_at: datetime = Field(
        sa_column=Column(postgresql.TIMESTAMP, default=datetime.now)
    )


class Consumer(UserBase, table=True):
    id: UUID = Field(
        sa_column=Column(postgresql.UUID, primary_key=True, default=uuid4),
    )
    email_verified: bool = Field(default=True)
    orders: list[Order] = Relationship(
        back_populates="consumer", sa_relationship_kwargs={"lazy": "selectin"}
    )
    created_at: datetime = Field(
        sa_column=Column(postgresql.TIMESTAMP, default=datetime.now)
    )


class Review(SQLModel, table=True):
    id: UUID = Field(
        sa_column=Column(postgresql.UUID, primary_key=True, default=uuid4),
    )
    rating: int = Field(ge=1, le=5)
    comment: str | None = Field(None)
    order_id: UUID = Field(foreign_key="order.id")
    order: Order = Relationship(
        back_populates="review", sa_relationship_kwargs={"lazy": "selectin"}
    )
    created_at: datetime = Field(
        sa_column=Column(postgresql.TIMESTAMP, default=datetime.now)
    )


# TODO slightly modified token also allows seller to add venue.. wtf?
