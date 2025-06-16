from datetime import timedelta
from typing import Generic, Type, TypeVar
from uuid import UUID

from fastapi import BackgroundTasks
from passlib.context import CryptContext
from pydantic import EmailStr
from sqlalchemy import select

from app.api.schemas.user import UserCreate, UserUpdate
from app.config import app_settings
from app.core.exceptions import (
    AccountNotVerified,
    BadCredentials,
    EmailAlreadyRegistered,
    EntityNotFound,
    InvalidToken,
)
from app.database.models import UserBase
from app.services.base import BaseService
from app.services.notification import NotificationService
from app.utils import (
    decode_url_safe_token,
    generate_access_token,
    generate_url_safe_token,
)

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

Model = TypeVar("Model", bound=UserBase)
CreateModel = TypeVar("CreateModel", bound=UserCreate)
UpdateModel = TypeVar("UpdateModel", bound=UserUpdate)


class UserService(Generic[Model, CreateModel, UpdateModel], BaseService[Model]):
    def __init__(self, model: Type[Model], session, tasks: BackgroundTasks):
        super().__init__(model=model, session=session)
        self.notification_service = NotificationService(tasks=tasks)

    async def _add_user(self, data: dict, router_prefix: str) -> Model:
        user = self.model(**data, password_hash=password_context.hash(data["password"]))
        await self._check_if_already_registered(email=data["email"])
        user = await self._add(user)
        token = generate_url_safe_token({"email": user.email, "id": str(user.id)})
        await self.notification_service.send_email_with_template(
            recipients=[user.email],
            subject="Account Confirmation",
            context={
                "username": user.name,
                "verification_url": f"http://{app_settings.APP_DOMAIN}{router_prefix}/verify?token={token}",
            },
            template_name="mail_email_verify.html",
        )
        return user

    async def update(self, id: UUID, user_update: UpdateModel) -> Model:
        user = await self._get(id)
        if not user:
            raise EntityNotFound()
        user.sqlmodel_update(user_update.model_dump(exclude_none=True))
        await self._update(user)

        return user

    async def verify_email(self, token: str) -> None:
        token_data = decode_url_safe_token(token)
        if token_data is None:
            raise InvalidToken()
        user = await self._get(UUID(token_data["id"]))
        user.email_verified = True
        await self._update(user)

    async def _get_by_email(self, email: str) -> Model:
        return await self.session.scalar(
            select(self.model).where(self.model.email == email)  # type: ignore
        )

    async def _check_if_already_registered(self, email: EmailStr):
        entity = await self._get_by_email(email=email)
        if entity is not None:
            raise EmailAlreadyRegistered()

    async def _generate_token(self, email: str, password: str) -> str:
        entity = await self._get_by_email(email)
        if entity is None or not password_context.verify(
            password, entity.password_hash
        ):
            raise BadCredentials()
        if not entity.email_verified:
            raise AccountNotVerified()
        token = generate_access_token(data={"user": {"id": str(entity.id)}})

        return token

    async def send_password_reset_link(self, email, router_prefix) -> None:
        user = await self._get_by_email(email)
        token = generate_url_safe_token({"id": str(user.id)}, "reset-password")

        await self.notification_service.send_email_with_template(
            recipients=[user.email],
            subject="Reset Password",
            context={
                "user": user.name,
                "link": f"http://{app_settings.APP_DOMAIN}{router_prefix}/reset_password_form?token={token}",
            },
            template_name="mail_password_reset.html",
        )

    async def reset_password(self, token: str, password: str) -> None:
        token_data = decode_url_safe_token(
            token=token, salt="reset-password", expiry=timedelta(days=1)
        )
        if token_data is None:
            raise InvalidToken()
        user = await self._get(UUID(token_data["id"]))
        user.password_hash = password_context.hash(password)
        await self._update(user)
