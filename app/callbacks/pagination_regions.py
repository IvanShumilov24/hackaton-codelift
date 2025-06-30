from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton
from loguru import logger

from app.database.models.place import Place
from app.handlers.commands import get_all_regions_command
from app.services.place_service import PlaceService
from app.services.region_service import RegionService
from app.utils.functions import handle_telegram_edit_error
from app.utils.pagination import Pagination
from app.utils.statekeys import StateKeys

router = Router(name="Regions pagination router")


@router.callback_query(F.data == StateKeys.REGIONS)
async def handle_regions_list_request(
        callback: CallbackQuery,
        state: FSMContext,
        region_service: RegionService,
) -> None:
    try:
        await get_all_regions_command(
            message=callback.message,
            region_service=region_service,
            state=state,
            is_edited=True
        )
    except Exception as e:
        logger.error(f"Ошибка при выводе регионов: {e}")


@router.callback_query(F.data.startswith("regions:"), F.data.split(":")[1].isdigit())
async def handle_region_places(
        callback: CallbackQuery,
        state: FSMContext,
        place_service: PlaceService,
) -> None:
    try:
        region_id = int(callback.data.split(":")[1])
        places: list[Place] = await place_service.get_all_by_region_id(region_id)

        places_pagination = Pagination(
            data=places,
            item_format=lambda place: place.title,
            item_callback=lambda place, prefix: f"{prefix}:{place.place_id}"
        )

        await state.update_data({StateKeys.PLACES_PAGINATION: places_pagination})
        await state.update_data({StateKeys.PLACES: places})

        keyboard = await places_pagination.get_page_keyboard(
            prefix=StateKeys.PLACES.value,
            additional_buttons=[InlineKeyboardButton(text="Регионы", callback_data=StateKeys.REGIONS),
                                InlineKeyboardButton(text="Главное меню", callback_data=StateKeys.MAIN_MENU)],
        )

        await callback.message.edit_text(
            text="Вот места:",
            reply_markup=keyboard,
        )
    except Exception as e:
        logger.error(f"Ошибка при выводе региона: {e}")


@router.callback_query(
    F.data.startswith("regions:"),
    lambda query: query.data.split(":")[1] in ("prev", "next")
)
async def handle_regions_pagination(callback: CallbackQuery, state: FSMContext) -> None:
    try:
        pagination = await state.get_value(StateKeys.REGIONS_PAGINATION)

        old_page = pagination.current_page
        new_page = await pagination.process_callback(callback.data)

        if old_page == new_page:
            await callback.answer()
            return

        keyboard = await pagination.get_page_keyboard(
            prefix=StateKeys.REGIONS.value,
            additional_buttons=[InlineKeyboardButton(text="Главное меню", callback_data=StateKeys.MAIN_MENU)],
        )

        await state.update_data({StateKeys.REGIONS_PAGINATION: pagination})

        await callback.message.edit_text(
            f"Вот регионы:",
            reply_markup=keyboard
        )
        await callback.answer()
    except TelegramBadRequest as e:
        await handle_telegram_edit_error(callback=callback, error=e)
    except Exception as e:
        logger.error(f"Ошибка при пагинации мест: {e}")
