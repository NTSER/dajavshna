from uuid import UUID

from fastapi import APIRouter

from app.api.dependencies import ConsumerDep, OrderServiceDep, VenueServiceDep
from app.api.schemas.order import OrderCreate, OrderPublic

router = APIRouter(prefix="/order", tags=["Order"])


@router.post("/add", response_model=OrderPublic)
async def add_order(
    venue_id: UUID,
    order: OrderCreate,
    service: OrderServiceDep,
    venue_service: VenueServiceDep,
    consumer: ConsumerDep,
):
    venue = await venue_service.get(venue_id)
    return await service.add(order, venue=venue, consumer=consumer)
