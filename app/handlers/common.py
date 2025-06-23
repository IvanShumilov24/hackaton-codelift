from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.database.models.region import Region
from app.keyboards.builders import create_inline_keyboard
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
        await user_service.register_user(
            user_id=message.from_user.id,
            first_name=message.from_user.first_name,
        )

        await message.answer(
            text=f"Привет {message.from_user.first_name}! Приветствуем тебя в нашем путеводителе по ЛО",
            reply_markup=await create_inline_keyboard([("Перейти к списку", "regions")])
        )

    except Exception as e:
        logger.error(f"Ошибка при обработке /start: {e}")
        await message.answer("⚠️ Произошла ошибка при регистрации. Попробуйте позже.")
