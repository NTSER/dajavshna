from uuid import UUID

from fastapi import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.order import OrderCreate, OrderItemCreate
from app.database.models import Consumer, Order, OrderItem, Venue
from app.services.notification import NotificationService

from .base import BaseService


class OrderService(BaseService[Order]):
    def __init__(self, session: AsyncSession, tasks: BackgroundTasks):
        super().__init__(Order, session)  # type: ignore
        self.notification_service = NotificationService(tasks=tasks)

    async def get(self, id: UUID) -> Order:
        return await self._get(id)

    async def _add_item(
        self, order_item_create: OrderItemCreate, order_id: UUID
    ) -> OrderItem:
        order_item = OrderItem(**order_item_create.model_dump(), order_id=order_id)

        self.session.add(order_item)
        await self.session.commit()
        await self.session.refresh(order_item)
        return order_item

    async def add(self, order: OrderCreate, venue: Venue, consumer: Consumer) -> Order:
        new_order = Order(
            **order.model_dump(exclude={"order_items"}),
            venue_id=venue.id,
            consumer_id=consumer.id,
        )
        await self._add(new_order)
        for order_item_create in order.order_items:
            await self._add_item(
                order_item_create=order_item_create, order_id=new_order.id
            )
        await self.notification_service.send_email_with_template(
            recipients=[consumer.email],
            subject="Successful Order",
            context={
                "venue": venue.name,
                "consumer": consumer.name,
                "datetime": order.reservation_time,
            },
            template_name="mail_order.html",
        )
        return new_order

    async def update(self, id: UUID, update_dict: dict) -> Order:
        order = await self.get(id)
        order.sqlmodel_update(update_dict)
        return await self._update(order)

    async def delete(self, id: UUID) -> Order:
        order = await self.get(id)
        await self._delete(order)
        return order
