from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton

from app.database.models.region import Region
from app.handlers.common import start_handler
from app.services.place_service import PlaceService
from app.services.region_service import RegionService
from app.services.user_service import UserService
from app.utils.logger import logger
from app.utils.pagination import Pagination

router = Router()


@router.message(Command("regions"))
async def get_all_regions_command(
        message: Message,
        region_service: RegionService,
        state: FSMContext,
        is_edited: bool = False,
):
    await state.clear()
    regions = await region_service.get_all_regions()

    regions_pagination = Pagination(
        data=regions,
        item_format=lambda region: region.name,
        item_callback=lambda region: f"regions:{region.region_id}",
    )

    await state.update_data(regions_pagination=regions_pagination)
    await state.update_data(regions=regions)

    keyboard = await regions_pagination.get_page_keyboard(
        prefix="regions",
        additional_buttons=[InlineKeyboardButton(text="Главное меню", callback_data="main_menu")],
    )

    if is_edited:
        await message.edit_text(text="Вот список регионов:", reply_markup=keyboard)
        return
    await message.answer(text="Вот список регионов:", reply_markup=keyboard)


