from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class Pagination:
    def __init__(self, data: list, page_size: int = 5):
        self.data = data
        self.page_size = page_size
        self.current_page = 1
        self.total_pages = (len(data) + page_size - 1) // page_size

    def get_current_page_data(self):
        start = (self.current_page - 1) * self.page_size
        end = start + self.page_size
        return self.data[start:end]

    async def get_page_keyboard(self, prefix: str):
        builder = InlineKeyboardBuilder()

        for item in self.get_current_page_data():
            name = item['name']
            builder.row(InlineKeyboardButton(
                text=name,
                callback_data=f"{prefix}:reg:{name}"
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

        return builder.as_markup()

    async def process_callback(self, callback_data: str):
        action = callback_data.split(":")[1]

        if action == "prev" and self.current_page > 1:
            self.current_page -= 1
        elif action == "next" and self.current_page < self.total_pages:
            self.current_page += 1

        return self.current_page
