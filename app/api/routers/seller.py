from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr

from app.api.dependencies import SellerAccessTokenDep, SellerDep, SellerServiceDep
from app.api.schemas.seller import SellerCreate, SellerPublic, SellerUpdate
from app.database.redis import add_jti_to_redis

router = APIRouter(prefix="/seller", tags=["Seller"])


@router.post("/add", response_model=SellerPublic)
async def add_seller(seller: SellerCreate, service: SellerServiceDep):
    seller_public = await service.add(seller)
    return seller_public


@router.patch("/update")
async def update_seller(
    seller: SellerDep, seller_update: SellerUpdate, service: SellerServiceDep
):
    return await service.update(seller.id, seller_update)


@router.get("/verify")
async def verify_email(token: str, service: SellerServiceDep):
    await service.verify_email(token)
    return {"detail": "Account verified"}


@router.get("/forgot_password")
async def forgot_password(email: EmailStr, service: SellerServiceDep):
    await service.send_password_reset_link(email, router.prefix)
    return {"detail": "Check email for password reset link"}


@router.get("/reset_password")
async def reset_password(token: str, password: str, service: SellerServiceDep):
    await service.reset_password(token, password)
    return {"detail": "Successfully reseted password"}


@router.post("/token")
async def token(
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: SellerServiceDep,
):
    token = await service.token(request_form.username, request_form.password)
    return {"access_token": token, "type": "jwt"}


@router.get("/logout")
async def logout_seller(token: SellerAccessTokenDep):
    await add_jti_to_redis(token["jti"])
    return {"message": "logged out successfully"}
