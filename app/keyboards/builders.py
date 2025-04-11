from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


async def create_inline_keyboard(buttons: list[tuple[str, str]]) -> InlineKeyboardMarkup:
    """
    Создает inline клавиатуру.

    :param buttons: Список кортежей [(текст кнопки, callback_data), (..., ...)]
    :return: Объект InlineKeyboardMarkup
    """
    builder = InlineKeyboardBuilder()
    for text, callback_data in buttons:
        builder.button(text=text, callback_data=callback_data)
    return builder.as_markup()


async def create_reply_keyboard(buttons: list[str]) -> ReplyKeyboardMarkup:
    """
    Создает reply клавиатуру.

    :param buttons: Список названий [текст кнопки, ...]
    :return: Объект ReplyKeyboardMarkup
    """
    builder = ReplyKeyboardBuilder()
    [builder.button(text=txt) for txt in buttons]

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
