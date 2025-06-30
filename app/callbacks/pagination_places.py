import uuid
from typing import Union

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton
from loguru import logger

from app.database.models.place import Place
from app.keyboards.builders import create_inline_keyboard
from app.utils.functions import is_valid_uuid, handle_telegram_edit_error


async def get_place_from_state(callback: CallbackQuery, state: FSMContext) -> Union[Place, None]:
    try:
        place_id_str = callback.data.split(":")[1]
        place_id = uuid.UUID(place_id_str)
    except (IndexError, ValueError):
        return None

    places: list[Place] | Place = await state.get_value("places")
    if not places:
        return None

    return next((place for place in places if place.place_id == place_id), None)


router = Router(name="Places pagination router")


@router.callback_query(
    F.data.startswith("places:"),
    lambda query: is_valid_uuid(query.data.split(":")[1])
)
async def get_detail_info_place(
        callback: CallbackQuery,
        state: FSMContext,
):
    place: Place = await get_place_from_state(callback=callback, state=state)
    if place is None:
        msg = "Место не найдено!"
        logger.error(msg)
        await callback.answer(text=msg, show_alert=True)
        return

    await callback.message.edit_text(
        text=f"📍 *{place.title}*\n\n"
             f"📜 *Описание:*\n"
             f"{place.description}",
        reply_markup=await create_inline_keyboard(
            [("⬅️ Назад", "back_to_places_list")]
        ),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(
    F.data.startswith("places:"),
    lambda query: query.data.split(":")[1] in ("prev", "next")
)
async def handle_places_pagination(callback: CallbackQuery, state: FSMContext):
    try:
        pagination = await state.get_value("places_pagination")

        old_page = pagination.current_page
        new_page = await pagination.process_callback(callback.data)

        if old_page == new_page:
            await callback.answer()
            return

        keyboard = await pagination.get_page_keyboard(
            prefix="places",
            additional_buttons=[InlineKeyboardButton(text="Регионы", callback_data="regions")],
        )

        await state.update_data(places_pagination=pagination)
        await callback.message.edit_text(
            text=f"Вот места:",
            reply_markup=keyboard
        )
        await callback.answer()
    except TelegramBadRequest as e:
        await handle_telegram_edit_error(callback=callback, error=e)
    except Exception as e:
        logger.error(f"Ошибка при пагинации мест: {e}")


@router.callback_query(F.data == "back_to_places_list")
async def return_to_places_list(callback: CallbackQuery, state: FSMContext):
    try:
        pagination = await state.get_value("places_pagination")

        keyboard = await pagination.get_page_keyboard(
            prefix="places",
            additional_buttons=[InlineKeyboardButton(text="Регионы", callback_data="regions"),
                                InlineKeyboardButton(text="Главное меню", callback_data="main_menu")],
        )
        await callback.message.edit_text(f"Вот места:", reply_markup=keyboard)
    except Exception as e:
        logger.error(f"Ошибка при возвращении к списку мест: {e}")
