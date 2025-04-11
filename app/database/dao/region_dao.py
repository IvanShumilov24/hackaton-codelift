from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.region import Region
from app.database.models.user import User
from app.utils.logger import logger


class RegionDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_one_or_none(self, region_id: int) -> Region | None:
        try:
            query = select(Region).where(Region.region_id == region_id)
            result = await self.session.execute(query)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при получении региона {region_id}: {e}")
            await self.session.rollback()
            raise

    async def get_all(self, region_id: int, offset: int = 10) -> Region | None:
        try:
            query = select(Region).offset().order_by(Region.name)
            result = await self.session.execute(query)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при получении региона {region_id}: {e}")
            await self.session.rollback()
            raise

