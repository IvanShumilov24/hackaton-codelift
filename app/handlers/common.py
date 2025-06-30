from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

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
        is_edited: bool = False,
        user_id: int = None,
        first_name: str = None,
):
    try:
        if user_id and first_name:
            await user_service.register_user(
                user_id=int(user_id),
                first_name=first_name,
            )
        else:
            await user_service.register_user(
                user_id=int(message.from_user.id),
                first_name=message.from_user.first_name,
            )

        if is_edited:
            await message.edit_text(
                text=f"Приветствуем тебя в нашем путеводителе по ЛО",
                reply_markup=await create_inline_keyboard([("Перейти к списку", "regions")])
            )
            return

        await message.answer(
            text=f"Приветствуем тебя в нашем путеводителе по ЛО",
            reply_markup=await create_inline_keyboard([("Перейти к списку", "regions")])
        )

    except Exception as e:
        logger.error(f"Ошибка при обработке /start: {e}")
        await message.answer("⚠️ Произошла ошибка при регистрации. Попробуйте позже.")


@router.callback_query(F.data == "main_menu")
async def main_menu_handler(
        callback: CallbackQuery,
        user_service: UserService,
):
    await start_handler(
        message=callback.message,
        user_service=user_service,
        is_edited=True,
        user_id=callback.from_user.id,
        first_name=callback.from_user.first_name,
    )
