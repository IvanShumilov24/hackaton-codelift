from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Callable, Optional


class Pagination:
    def __init__(
            self,
            data: list,
            page_size: int = 5,
            item_format: Callable = lambda item: f"Item {getattr(item, 'id', '')}",
            item_callback: Callable = lambda item, prefix: f"item:{prefix}:{getattr(item, 'id', '')}"
    ):
        self.data = data
        self.page_size = page_size
        self.current_page = 1
        self.total_pages = max((len(data) + page_size - 1) // page_size, 1)  # Не меньше 1
        self.item_format = item_format
        self.item_callback = item_callback

    def get_current_page_data(self) -> list:
        start = (self.current_page - 1) * self.page_size
        end = start + self.page_size
        return self.data[start:end]

    async def get_page_keyboard(self, prefix: str, additional_buttons: Optional[list[InlineKeyboardButton]] = None) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()

        # Добавляем кнопки с данными текущей страницы
        for item in self.get_current_page_data():
            builder.row(InlineKeyboardButton(
                text=self.item_format(item),
                callback_data=self.item_callback(item, prefix)
            ))

        pagination_buttons = []
        if self.current_page > 1:
            pagination_buttons.append(InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data=f"{prefix}:prev"
            ))

        pagination_buttons.append(InlineKeyboardButton(
            text=f"{self.current_page}/{self.total_pages}",
            callback_data=f"{prefix}:page"
        ))

        if self.current_page < self.total_pages:
            pagination_buttons.append(InlineKeyboardButton(
                text="Вперёд ➡️",
                callback_data=f"{prefix}:next"
            ))

        builder.row(*pagination_buttons)

        if additional_buttons:
            for button in additional_buttons:
                builder.row(button)

        return builder.as_markup()

    async def process_callback(self, callback_data: str) -> int:
        action = callback_data.split(":")[1]

        if action == "prev" and self.current_page > 1:
            self.current_page -= 1
        elif action == "next" and self.current_page < self.total_pages:
            self.current_page += 1

        return self.current_page
