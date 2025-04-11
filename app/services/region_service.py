from app.database.dao.region_dao import RegionDAO
from app.database.models.region import Region
from app.utils.logger import logger


class RegionService:
    def __init__(self, region_dao: RegionDAO):
        self.region_dao = region_dao

    async def get_all_regions(self) -> list[Region]:
        try:
            regions = await self.region_dao.get_all()
            logger.success(f"Найдено {len(regions)} регионов")
            return regions
        except Exception as e:
            logger.error(f"Ошибка получения всех регионов: {e}")
            raise

    async def get_one_region(self, region_id: int) -> Region:
        try:
            region = await self.region_dao.get_one_or_none(region_id)
            if not region:
                raise ValueError("Регион не найден")
            return region
        except Exception as e:
            logger.error(f"Ошибка получения региона {region_id}: {e}")
            raise
