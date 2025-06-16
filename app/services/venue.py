from typing import Sequence
from uuid import UUID

from fastapi import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.venue import VenueCreate, VenuePublic
from app.database.models import Seller, Venue, VenueImage

from .base import BaseImageService, BaseService


class VenueService(BaseService[Venue]):
    def __init__(self, session: AsyncSession):
        super().__init__(Venue, session)  # type: ignore

    async def get(self, id: UUID) -> Venue:
        return await self._get(id)

    async def list(self, public: VenuePublic) -> Sequence[Venue]:
        return await self._filter(public.model_dump())

    async def add(self, venue: VenueCreate, seller: Seller) -> Venue:
        new_venue = Venue(**venue.model_dump(), seller_id=seller.id)
        return await self._add(new_venue)

    async def update(self, id: UUID, update_dict: dict) -> Venue:
        venue = await self.get(id)
        venue.sqlmodel_update(update_dict)
        return await self._update(venue)

    async def delete(self, id: UUID) -> Venue:
        venue = await self.get(id)
        await self._delete(venue)
        return venue


class VenueImageService(BaseImageService[VenueImage]):
    def __init__(self, session, tasks: BackgroundTasks):
        super().__init__(VenueImage, session, tasks)
