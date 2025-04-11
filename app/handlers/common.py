from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from app.services.user_service import UserService
from app.utils.logger import logger
from app.utils.pagination import Pagination

router = Router()

user_pagination = {}

lst = [{"name": "Волосовский"},
       {"name": "Волховский"},
       {"name": "Всеволожский"},
       {"name": "Выборгский"},
       {"name": "Кингисеппский"},
       {"name": "Киришский"},
       {"name": "Кировский"},
       {"name": "Лодейнопольский"},
       {"name": "Ломоносовский"},
       {"name": "Лужский"},
       {"name": "Подпорожский"},
       {"name": "Приозерский"},
       {"name": "Сланцевский"},
       {"name": "Тихвинский"},
       {"name": "Тосненский"},
       {"name": "Сосновоборский"},
       {"name": "Гатчинский"},
       {"name": "Бокситогорский"}]


@router.message(CommandStart())
async def start_handler(
        message: Message,
        user_service: UserService,
):
    try:
        user = await user_service.register_user(
            user_id=message.from_user.id,
            first_name=message.from_user.first_name,
        )
        await message.answer(f"Привет {message.from_user.first_name}! Приветствуем тебя в нашем путеводителе по ЛО")

        pagination = Pagination(lst)
        user_pagination[message.from_user.id] = pagination

        keyboard = await pagination.get_page_keyboard(prefix="regions")

        await message.answer(
            "Список регионов:",
            reply_markup=keyboard
        )

    except Exception as e:
        logger.error(f"Ошибка при обработке /start: {e}")
        await message.answer("⚠️ Произошла ошибка при регистрации. Попробуйте позже.")
