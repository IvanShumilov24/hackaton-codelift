from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton

from app.database.models.place import Place
from app.handlers.commands import get_all_regions_command
from app.services.place_service import PlaceService
from app.services.region_service import RegionService
from app.utils.pagination import Pagination

router = Router(name="Regions pagination router")


@router.callback_query(F.data == "regions")
async def handle_regions_list_request(
        callback: CallbackQuery,
        state: FSMContext,
        region_service: RegionService,
):
    await get_all_regions_command(
        message=callback.message,
        region_service=region_service,
        state=state,
        is_edited=True
    )


@router.callback_query(
    F.data.startswith("regions:"),
    lambda query: query.split(":")[1].isdigit()
)
async def get_detail_region(
        callback: CallbackQuery,
        state: FSMContext,
        place_service: PlaceService,
):
    region_id = int(callback.data.split(":")[1])
    places: list[Place] = await place_service.get_all_by_region_id(region_id)

    places_pagination = Pagination(
        data=places,
        item_format=lambda place: place.name,
        item_callback=lambda place, prefix: f"{prefix}:{place.place_id}"
    )

    await state.update_data(places_pagination=places_pagination)
    await state.update_data(places=places)

    keyboard = await places_pagination.get_page_keyboard(
        prefix="places",
        additional_buttons=[InlineKeyboardButton(text="Регионы", callback_data="regions"),
                            InlineKeyboardButton(text="Главное меню", callback_data="main_menu")],
    )

    await callback.message.edit_text(
        text="Вот места:",
        reply_markup=keyboard,
    )
