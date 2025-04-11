from app.database.dao import place_dao
from app.database.dao.place_dao import PlaceDAO
from app.database.models.place import Place
from app.utils.logger import logger


class PlaceService:
    def __init__(self, place_dao: PlaceDAO):
        self.place_dao = place_dao

    async def get_all_by_region_id(self, region_id: int) -> list[Place]:
        try:
            all_places = await place_dao.get_all()
            places_by_region = [place for place in all_places if place.region_id == region_id]
            logger.info(f"Найдено {len(places_by_region)} мест региона")
            return places_by_region
        except Exception as e:
            logger.error(f"Ошибка при получении мест региона: {e}")
            raise

    async def get_one_place(self, place_id: int) -> Place:
        try:
            place = await place_dao.get_one_or_none(place_id)
            if not place:
                raise ValueError("Место не найдено")
            return place
        except Exception as e:
            logger.error(f"Ошибка получения места {place_id}: {e}")
            raise
