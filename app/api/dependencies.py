from typing import Annotated, Type
from uuid import UUID

from fastapi import BackgroundTasks, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import InvalidToken
from app.core.security import consumer_oath2_scheme, seller_oath2_scheme
from app.database.models import Consumer, Seller
from app.database.redis import is_jti_blacklisted
from app.database.session import get_session
from app.services.consumer import ConsumerService
from app.services.order import OrderService
from app.services.product import ProductImageService, ProductService
from app.services.seller import SellerService
from app.services.venue import VenueImageService, VenueService
from app.utils import decode_access_token

sessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_seller_service(session: sessionDep, tasks: BackgroundTasks) -> SellerService:
    return SellerService(session=session, tasks=tasks)


def get_consumer_service(
    session: sessionDep, tasks: BackgroundTasks
) -> ConsumerService:
    return ConsumerService(session=session, tasks=tasks)


def get_product_service(session: sessionDep) -> ProductService:
    return ProductService(session=session)


def get_venue_service(session: sessionDep) -> VenueService:
    return VenueService(session=session)


def get_order_service(session: sessionDep, tasks: BackgroundTasks) -> OrderService:
    return OrderService(session=session, tasks=tasks)


def get_product_image_service(session: sessionDep, tasks: BackgroundTasks):
    return ProductImageService(session=session, tasks=tasks)


def get_venue_image_service(session: sessionDep, tasks: BackgroundTasks):
    return VenueImageService(session=session, tasks=tasks)


SellerServiceDep = Annotated[SellerService, Depends(get_seller_service)]
ConsumerServiceDep = Annotated[ConsumerService, Depends(get_consumer_service)]
ProductServiceDep = Annotated[ProductService, Depends(get_product_service)]
VenueServiceDep = Annotated[VenueService, Depends(get_venue_service)]
OrderServiceDep = Annotated[OrderService, Depends(get_order_service)]
ProductImageServiceDep = Annotated[
    ProductImageService, Depends(get_product_image_service)
]
VenueImageServiceDep = Annotated[VenueImageService, Depends(get_venue_image_service)]


async def _get_access_token(
    token: str,
    session: sessionDep,
    model: Type,
) -> dict:
    data = decode_access_token(token)
    if (
        (data is None)
        or (await is_jti_blacklisted(data["jti"]))
        or (not await session.get(model, data["user"]["id"]))
    ):
        raise InvalidToken()

    return data


async def get_seller_access_token(
    token: Annotated[str, Depends(seller_oath2_scheme)], session: sessionDep
) -> dict:
    return await _get_access_token(token, session, Seller)


async def get_consumer_access_token(
    token: Annotated[str, Depends(consumer_oath2_scheme)], session: sessionDep
) -> dict:
    return await _get_access_token(token, session, Consumer)


ConsumerAccessTokenDep = Annotated[dict, Depends(get_consumer_access_token)]
SellerAccessTokenDep = Annotated[dict, Depends(get_seller_access_token)]


async def get_current_seller(
    token_data: SellerAccessTokenDep, session: sessionDep
) -> Seller | None:
    return await session.get(Seller, UUID(token_data["user"]["id"]))


async def get_current_consumer(
    token_data: ConsumerAccessTokenDep, session: sessionDep
) -> Consumer | None:
    return await session.get(Consumer, UUID(token_data["user"]["id"]))


SellerDep = Annotated[Seller, Depends(get_current_seller)]
ConsumerDep = Annotated[Consumer, Depends(get_current_consumer)]
