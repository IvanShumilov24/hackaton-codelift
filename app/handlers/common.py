from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.services.user_service import UserService
from app.utils.logger import logger

router = Router()


@router.message(Command("start"))
async def start_handler(
        message: Message,
        user_service: UserService,
):
    try:
        user = await user_service.register_user(
            id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name
        )
        await message.answer(
            f"ТАК НАХУЙ, {user.first_name} ДОБРО ПОЖАЛОВАТЬ В НАШУ КАЧАЛКУ"
            f"\n\n"
            f"ТУТ МЫ УЧИМ МУЖИКОВ КАК ПРАВИЛЬНО ТЯГАТЬ КОД СИДЯ, ПРОЕКТИРОВАТЬ БЕЛКОВУЮ АРХИТЕКТУРУ И НАРАЩИВАТЬ ТЕСТОВУЮ МАССУ")
    except Exception as e:
        logger.error(f"Ошибка при обработке /start: {e}")
        await message.answer("⚠️ Произошла ошибка при регистрации. Попробуйте позже.")
