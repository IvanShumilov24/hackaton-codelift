from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.utils.logger import logger

router = Router()


@router.callback_query(F.data.startswith("regions:reg:"))
async def get_regions(callback: CallbackQuery):
    region_id = int(callback.data.split(":")[-1])
    await callback.answer(f"Выбран регион {region_id}")


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
