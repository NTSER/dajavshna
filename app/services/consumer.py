from fastapi import BackgroundTasks
from app.api.schemas.consumer import ConsumerCreate, ConsumerUpdate
from app.database.models import Consumer
from app.services.user import UserService


class ConsumerService(UserService[Consumer, ConsumerCreate, ConsumerUpdate]):
    def __init__(self, session, tasks: BackgroundTasks):
        super().__init__(Consumer, session, tasks)

    async def add(self, consumer_create: ConsumerCreate) -> Consumer:
        return await self._add_user(consumer_create.model_dump(), "/consumer")

    async def token(self, email, password) -> str:
        return await self._generate_token(email=email, password=password)
