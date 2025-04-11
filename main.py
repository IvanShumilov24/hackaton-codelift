import logging

from aiogram.types import ErrorEvent

from app.database.dao.place_dao import PlaceDAO
from app.database.dao.region_dao import RegionDAO
from app.database.dao.user_dao import UserDAO
from app.handlers import common
from app.callbacks import pag_regs
from app.services.place_service import PlaceService
from app.services.region_service import RegionService
from app.utils.logger import logger
from config.config import Settings
from app.bot import create_bot
from app.database.base import Database
from app.services.user_service import UserService


async def main():
    logging.basicConfig(level=logging.INFO)

    config = Settings()
    bot, dp = await create_bot(config)
    database = Database(config.DB_URL)

    @dp.error()
    async def error_handler(event: ErrorEvent):
        logger.critical(
            f"Глобальная ошибка: {event.exception.__class__.__name__}: {event.exception}"
        )
        try:
            await event.update.message.answer(
                "⚠️ Произошла критическая ошибка."
            )
        except:
            pass

    @dp.update.middleware()
    async def di_middleware(handler, event, data):
        async with database.session_maker() as session:
            data["user_service"] = UserService(UserDAO(session))
            data["user_dao"] = UserDAO(session)
            data["region_service"] = RegionService(RegionDAO(session))
            data["region_dao"] = RegionDAO(session)
            data["place_service"] = PlaceService(PlaceDAO(session))
            data["place_dao"] = PlaceDAO(session)
            try:
                return await handler(event, data)
            except Exception as e:
                logger.error(f"Ошибка middleware: {e}")
                raise

    dp.include_router(common.router)
    dp.include_router(pag_regs.router)

    try:
        logger.info("Запуск бота...")
        await dp.start_polling(bot)
    except Exception as e:
        logger.critical(f"Бот остановлен: {e}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
