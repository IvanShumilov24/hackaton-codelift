from pydantic.v1 import UUID4
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.place import Place
from app.utils.logger import logger


class PlaceDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_one_or_none(self, place_id: UUID4) -> Place | None:
        try:
            query = select(Place).where(Place.place_id == place_id)
            result = await self.session.execute(query)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при получении места {place_id}: {e}")
            await self.session.rollback()
            raise e

    async def get_all(self, offset: int = 0, limit: int = 100) -> list[Place] | None:
        try:
            query = select(Place).offset(offset).limit(limit).order_by(Place.title)
            result = await self.session.execute(query)
            return result.scalars().all()
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при получении всех мест: {e}")
            await self.session.rollback()
            raise e
