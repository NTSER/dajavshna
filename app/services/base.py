import shutil
from pathlib import Path
from typing import Any, Generic, Sequence, Type, TypeVar
from uuid import UUID, uuid4

from fastapi import BackgroundTasks, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel

from app.core.exceptions import EntityNotFound
from app.database.base_models import ImageBase

Model = TypeVar("Model", bound=SQLModel)
ImageModel = TypeVar("ImageModel", bound=ImageBase)


class BaseService(Generic[Model]):
    def __init__(self, model: Type[Model], session: AsyncSession):
        self.model = model
        self.session = session

    async def _get(self, id: UUID) -> Model:
        entity = await self.session.get(self.model, id)
        if entity is None:
            raise EntityNotFound()
        return entity

    async def _filter(self, filters: dict[str, Any]) -> Sequence[Model]:
        stmt = select(self.model).where(
            *[
                getattr(self.model, key) == value
                for key, value in filters.items()
                if value is not None and hasattr(self.model, key)
            ]
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def _add(self, entity: Model) -> Model:
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity

    async def _update(self, entity: Model) -> Model:
        return await self._add(entity)

    async def _delete(self, entity: Model) -> None:
        await self.session.delete(entity)
        await self.session.commit()


class BaseImageService(BaseService[ImageModel]):
    def __init__(self, model: Type[ImageModel], session, tasks: BackgroundTasks):
        super().__init__(model=model, session=session)
        self.tasks = tasks
        self.storage_dir = Path("staticfiles")
        self.storage_dir.mkdir(exist_ok=True)

    def _build_file_path(self, original_filename: str) -> Path:
        ext = Path(original_filename).suffix
        unique_name = f"{uuid4()}{ext}"
        file_path = self.storage_dir / unique_name
        return file_path

    def _write_file(self, file: UploadFile, path: Path):
        with open(path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    async def _save_image(self, file: UploadFile) -> str:
        file_path = self._build_file_path(file.filename)  # type: ignore
        self.tasks.add_task(self._write_file, file, file_path)
        return str(file_path)

    async def add(self, file: UploadFile) -> ImageModel:
        image_path = await self._save_image(file=file)
        image = self.model(path=image_path)  # type: ignore
        return await self._add(image)
