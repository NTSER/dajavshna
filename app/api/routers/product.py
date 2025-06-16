from uuid import UUID

from fastapi import APIRouter, Query, UploadFile

from app.api.dependencies import (
    ProductImageServiceDep,
    ProductServiceDep,
    SellerDep,
    VenueServiceDep,
)
from app.api.schemas.product import ProductCreate, ProductPublic, ProductUpdate

router = APIRouter(prefix="/product", tags=["Product"])


@router.get("/list", response_model=list[ProductPublic])
async def list_products(
    service: ProductServiceDep,
    product_public: ProductPublic = Query(None),
):
    return await service.list(product_public)


@router.post("/add", response_model=ProductPublic)
async def add_product(
    venue_id: UUID,
    product: ProductCreate,
    service: ProductServiceDep,
    venue_service: VenueServiceDep,
    seller: SellerDep,
):
    venue = await venue_service.get(venue_id)
    return await service.add(product, venue=venue)


@router.patch("/update", response_model=ProductPublic)
async def update_product(
    id: UUID,
    update_product: ProductUpdate,
    service: ProductServiceDep,
    seller: SellerDep,
):
    return await service.update(
        id=id, update_dict=update_product.model_dump(exclude_none=True)
    )


@router.delete("/delete")
async def delete_product(
    id: UUID,
    service: ProductServiceDep,
    seller: SellerDep,
):
    await service.delete(id)
    return {"detail": "Deleted successfully"}


@router.post("/upload_image/")
async def upload_image(
    file: UploadFile, product_image_service: ProductImageServiceDep, seller: SellerDep
):
    return await product_image_service.add(file)


# TODO make sure seller which doesnt own product can not update it.
