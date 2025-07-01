from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from app.keyboards.builders import create_inline_keyboard
from app.services.user_service import UserService
from app.utils.logger import logger
from app.utils.statekeys import StateKeys

router = Router(name="Start router")


async def handle_user_start(
        message: Message,
        user_service: UserService,
        user_id: int,
        first_name: str,
        is_edited: bool = False,
):
    try:
        await user_service.register_user(user_id=user_id, first_name=first_name)

        text = "Приветствуем тебя в нашем путеводителе по ЛО"
        keyboard = await create_inline_keyboard([("Перейти к списку", "regions")])

        if is_edited:
            await message.edit_text(text=text, reply_markup=keyboard)
        else:
            await message.answer(text=text, reply_markup=keyboard)

    except Exception as e:
        logger.error(f"Ошибка при обработке /start: {e}")
        await message.answer("⚠️ Произошла ошибка при регистрации. Попробуйте позже.")


@router.message(CommandStart())
async def start_handler(message: Message, user_service: UserService):
    await handle_user_start(
        message=message,
        user_service=user_service,
        user_id=message.from_user.id,
        first_name=message.from_user.first_name
    )


@router.callback_query(F.data == StateKeys.MAIN_MENU)
async def main_menu_handler(callback: CallbackQuery, user_service: UserService):
    await handle_user_start(
        message=callback.message,
        user_service=user_service,
        user_id=callback.from_user.id,
        first_name=callback.from_user.first_name,
        is_edited=True
    )

