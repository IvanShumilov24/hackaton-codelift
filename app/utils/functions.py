from uuid import UUID
from loguru import logger
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery


def is_valid_uuid(uuid_str: str) -> bool:
    """Проверяет, является ли строка валидным UUID"""
    try:
        UUID(uuid_str)
        return True
    except ValueError:
        return False


async def handle_telegram_edit_error(callback: CallbackQuery, error: TelegramBadRequest) -> None:
    """Обрабатывает ошибки редактирования сообщений Telegram"""
    if "message is not modified" in str(error):
        await callback.answer()
        logger.debug("Message has not been changed")
    else:
        logger.error(f"Message editing error: {error}")
        raise
