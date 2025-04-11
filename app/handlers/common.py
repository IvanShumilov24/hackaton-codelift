from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.database.models.region import Region
from app.services.region_service import RegionService
from app.services.user_service import UserService
from app.utils.logger import logger
from app.utils.pagination import Pagination

router = Router()

lst = [{"region_id": 1, "name": "Волосовский"},
       {"region_id": 2, "name": "Волховский"},
       {"region_id": 3, "name": "Всеволожский"},
       {"region_id": 4, "name": "Выборгский"},
       {"region_id": 5, "name": "Кингисеппский"},
       {"region_id": 6, "name": "Киришский"},
       {"region_id": 7, "name": "Кировский"},
       {"region_id": 8, "name": "Лодейнопольский"},
       {"region_id": 9, "name": "Ломоносовский"},
       {"region_id": 10, "name": "Лужский"},
       {"region_id": 11, "name": "Подпорожский"},
       {"region_id": 12, "name": "Приозерский"},
       {"region_id": 13, "name": "Сланцевский"},
       {"region_id": 14, "name": "Тихвинский"},
       {"region_id": 15, "name": "Тосненский"},
       {"region_id": 16, "name": "Сосновоборский"},
       {"region_id": 17, "name": "Гатчинский"},
       {"region_id": 18, "name": "Бокситогорский"}]


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

        pagination = Pagination(region_list)
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
