from fastapi import BackgroundTasks
from app.api.schemas.seller import SellerCreate, SellerUpdate
from app.database.models import Seller
from app.services.user import UserService


class SellerService(UserService[Seller, SellerCreate, SellerUpdate]):
    def __init__(self, session, tasks: BackgroundTasks):
        super().__init__(Seller, session, tasks)

    async def add(self, seller_create: SellerCreate) -> Seller:
        return await self._add_user(seller_create.model_dump(), "/seller")

    async def token(self, email, password) -> str:
        return await self._generate_token(email=email, password=password)
