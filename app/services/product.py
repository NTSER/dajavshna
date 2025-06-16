from typing import Sequence
from uuid import UUID

from fastapi import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.product import ProductCreate, ProductPublic
from app.database.models import Product, ProductImage, Venue

from .base import BaseImageService, BaseService


class ProductService(BaseService[Product]):
    def __init__(self, session: AsyncSession):
        super().__init__(Product, session)  # type: ignore

    async def get(self, id: UUID) -> Product:
        return await self._get(id)

    async def list(self, public: ProductPublic) -> Sequence[Product]:
        return await self._filter(public.model_dump())

    async def add(self, product: ProductCreate, venue: Venue) -> Product:
        new_product = Product(**product.model_dump(), venue_id=venue.id)
        return await self._add(new_product)

    async def update(self, id: UUID, update_dict: dict) -> Product:
        product = await self.get(id)
        product.sqlmodel_update(update_dict)
        return await self._update(product)

    async def delete(self, id: UUID) -> Product:
        product = await self.get(id)
        await self._delete(product)
        return product


class ProductImageService(BaseImageService[ProductImage]):
    def __init__(self, session, tasks: BackgroundTasks):
        super().__init__(ProductImage, session, tasks)
