from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

import ssl
from app.config import db_settings

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE


engine = create_async_engine(
    url=db_settings.POSTGRES_URL,
    echo=True,
    connect_args={"ssl": ssl_context},
)


async def create_db_and_tables():
    async with engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)


async def get_session():
    async_session = sessionmaker(
        bind=engine,  # type: ignore
        class_=AsyncSession,
        expire_on_commit=False,
    )  # type: ignore
    async with async_session() as session:  # type: ignore
        yield session
