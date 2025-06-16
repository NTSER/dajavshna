from fastapi import APIRouter
from .routers import seller, consumer, product, venue, order

master_router = APIRouter()

master_router.include_router(seller.router)
master_router.include_router(consumer.router)
master_router.include_router(product.router)
master_router.include_router(venue.router)
master_router.include_router(order.router)
