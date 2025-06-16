from uuid import UUID

from fastapi import APIRouter, Query, UploadFile

from app.api.dependencies import (
    SellerDep,
    VenueImageServiceDep,
    VenueServiceDep,
)
from app.api.schemas.venue import VenueCreate, VenuePublic, VenueUpdate
from app.database.models import Venue

router = APIRouter(prefix="/venue", tags=["Venue"])


@router.get("/list", response_model=list[VenuePublic])
async def list_venue(
    service: VenueServiceDep,
    product_public: VenuePublic = Query(None),
):
    return await service.list(product_public)


@router.post("/add")
async def add_venue(
    venue: VenueCreate, service: VenueServiceDep, seller: SellerDep
) -> Venue:
    return await service.add(venue, seller)


@router.patch("/update", response_model=VenuePublic)
async def update_venue(
    id: UUID,
    update_venue: VenueUpdate,
    service: VenueServiceDep,
    seller: SellerDep,
):
    return await service.update(
        id=id, update_dict=update_venue.model_dump(exclude_none=True)
    )


@router.delete("/delete")
async def delete_venue(
    id: UUID,
    service: VenueServiceDep,
    seller: SellerDep,
):
    await service.delete(id)
    return {"detail": "Deleted successfully"}


@router.post("/upload_image/")
async def upload_image(
    file: UploadFile, venue_image_service: VenueImageServiceDep, seller: SellerDep
):
    return await venue_image_service.add(file)
