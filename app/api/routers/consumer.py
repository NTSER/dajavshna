from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr

from app.api.dependencies import ConsumerAccessTokenDep, ConsumerDep, ConsumerServiceDep
from app.api.schemas.consumer import ConsumerCreate, ConsumerPublic, ConsumerUpdate
from app.config import app_settings
from app.database.redis import add_jti_to_redis
from app.utils import TEMPLATE_DIR

router = APIRouter(prefix="/consumer", tags=["Consumer"])


@router.post("/add", response_model=ConsumerPublic)
async def add_consumer(consumer: ConsumerCreate, service: ConsumerServiceDep):
    consumer_public = await service.add(consumer)
    return consumer_public


@router.patch("/update")
async def update_consumer(
    consumer: ConsumerDep,
    consumer_update: ConsumerUpdate,
    service: ConsumerServiceDep,
):
    return await service.update(consumer.id, consumer_update)


@router.get("/verify")
async def verify_email(token: str, service: ConsumerServiceDep):
    await service.verify_email(token)
    return {"detail": "Account verified"}


@router.get("/forgot_password")
async def forgot_password(email: EmailStr, service: ConsumerServiceDep):
    await service.send_password_reset_link(email, router.prefix)
    return {"detail": "Check email for password reset link"}


@router.get("/reset_password_form")
async def get_reset_password_form(request: Request, token: str):
    templates = Jinja2Templates(TEMPLATE_DIR)
    return templates.TemplateResponse(
        request=request,
        name="reset_password.html",
        context={
            "reset_url": f"http://{app_settings.APP_DOMAIN}{router.prefix}/reset_password?token={token}"
        },
    )


@router.post("/reset_password")
async def reset_password(
    token: str, password: Annotated[str, Form()], service: ConsumerServiceDep
):
    await service.reset_password(token, password)
    return {"detail": "Successfully reseted password"}


@router.post("/token")
async def token(
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: ConsumerServiceDep,
):
    token = await service.token(request_form.username, request_form.password)
    return {"access_token": token, "type": "jwt"}


@router.get("/logout")
async def logout_consumer(token: ConsumerAccessTokenDep):
    await add_jti_to_redis(token["jti"])
    return {"message": "logged out successfully"}
