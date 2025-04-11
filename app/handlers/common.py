from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.database.models.region import Region
from app.services.region_service import RegionService
from app.services.user_service import UserService
from app.utils.logger import logger
from app.utils.pagination import Pagination

router = Router()


@router.message(CommandStart())
async def start_handler(
        message: Message,
        user_service: UserService,
        state: FSMContext,
        region_service: RegionService,
):
    try:
        user_pagination = {}

        region_list: list[Region] = await region_service.get_all_regions()

        await user_service.register_user(
            user_id=message.from_user.id,
            first_name=message.from_user.first_name,
        )

        await message.answer(f"Привет {message.from_user.first_name}! Приветствуем тебя в нашем путеводителе по ЛО")

        regions_data = [{"region_id": r.region_id, "name": r.name} for r in region_list]

        pagination = Pagination(regions_data)
        user_pagination[message.from_user.id] = pagination

        keyboard = await pagination.get_page_keyboard(prefix="regions")

        await state.update_data(user_pagination=user_pagination)

        await message.answer(
            "Выберите интересующий вас регион:",
            reply_markup=keyboard
        )

    except Exception as e:
        logger.error(f"Ошибка при обработке /start: {e}")
        await message.answer("⚠️ Произошла ошибка при регистрации. Попробуйте позже.")
