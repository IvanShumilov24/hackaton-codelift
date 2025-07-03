from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton
from loguru import logger

from app.services.region_service import RegionService
from app.utils.pagination import Pagination
from app.utils.statekeys import StateKeys

router = Router(name="Main commands router")


@router.message(Command("regions"))
async def get_all_regions_command(
        message: Message,
        region_service: RegionService,
        state: FSMContext,
        is_edited: bool = False,
):
    try:
        await state.clear()
        regions = await region_service.get_all_regions()

        regions_pagination = Pagination(
            data=regions,
            item_format=lambda region: region.name,
            item_callback=lambda region, prefix: f"{prefix}:{region.region_id}",
        )

        await state.update_data({StateKeys.REGIONS_PAGINATION: regions_pagination})
        await state.update_data({StateKeys.REGIONS: regions})

        keyboard = await regions_pagination.get_page_keyboard(
            prefix=StateKeys.REGIONS.value,
            additional_buttons=[InlineKeyboardButton(text="Главное меню", callback_data=StateKeys.MAIN_MENU)],
        )

        if is_edited:
            await message.edit_text(text="Вот список регионов:", reply_markup=keyboard)
            return
        await message.answer(text="Вот список регионов:", reply_markup=keyboard)
    except Exception as e:
        logger.exception(f"Ошибка в обраюотке команды /regions: {e}")

