from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.database.models.region import Region
from app.keyboards.builders import create_inline_keyboard
from app.services.place_service import PlaceService
from app.services.region_service import RegionService
from app.utils.logger import logger
from app.utils.pagination import Pagination

router = Router()


@router.callback_query(F.data == "back")
async def go_to_back(callback: CallbackQuery):
    await callback.message.delete()


@router.callback_query(F.data.startswith("places:reg:"))
async def get_regions(
        callback: CallbackQuery,
        state: FSMContext,
        place_service: PlaceService,
):
    try:
        await callback.answer()
        place_id = int(callback.data.split(":")[-1])

        place_info = await place_service.get_one_place(place_id)

        await callback.message.answer(
            text=f"{place_info.title}\n"
                 f"Описание:\n"
                 f"{place_info.description}",
            reply_markup=await create_inline_keyboard(
                [("Назад", "back")]
            )
        )
    except Exception as e:
        logger.error(f"Не удалось просмотреть места: {e}")


@router.callback_query(F.data.startswith("regions:reg:"))
async def get_regions(
        callback: CallbackQuery,
        region_service: RegionService,
        state: FSMContext,
        place_service: PlaceService,
):
    try:
        await callback.message.delete()
        await callback.answer()
        user_id = callback.from_user.id
        user_pagination = await state.get_value("user_pagination", None)

        if user_id not in user_pagination or user_pagination is None:
            await callback.answer("❌ Сессия устарела! Зайдите в список регионов заново")
            return

        region_id = int(callback.data.split(":")[-1])

        region_info = await region_service.get_one_region(region_id)

        region_places = await place_service.get_all_by_region_id(region_id)

        places_data = [{"title": r.title, "place_id": r.place_id} for r in region_places]

        pagination = Pagination(places_data)
        user_pagination[callback.from_user.id] = pagination

        keyboard = await pagination.get_page_keyboard(prefix="places")

        await state.update_data(user_pagination=user_pagination)

        await callback.message.answer(
            text=f"{region_info.name} район\n\n"
                 f"Описание:\n"
                 f"{region_info.description}\n\n"
                 f"Места:",
            reply_markup=keyboard
        )
    except Exception as e:
        logger.error(f"Ошибка в пагинации мест: {e}")


@router.callback_query(F.data.startswith("regions:"))
async def handle_pagination(callback: CallbackQuery, state: FSMContext):
    try:
        user_id = callback.from_user.id
        user_pagination = await state.get_value("user_pagination", None)

        if user_id not in user_pagination or user_pagination is None:
            await callback.answer("❌ Сессия устарела! Зайдите в список регионов заново")
            return

        pagination = user_pagination[user_id]

        await pagination.process_callback(callback.data)

        new_keyboard = await pagination.get_page_keyboard(prefix="regions")

        await callback.message.edit_reply_markup(reply_markup=new_keyboard)
        await callback.answer()
    except Exception as e:
        logger.error(f"Не получилось переключиться: {e}")
        await callback.message.answer("Ошибка при пагинации. Попробуйте нажать /start.")
