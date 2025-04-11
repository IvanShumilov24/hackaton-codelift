from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.database.models.region import Region
from app.handlers.common import start_handler
from app.services.region_service import RegionService
from app.services.user_service import UserService
from app.utils.logger import logger
from app.utils.pagination import Pagination

router = Router()


@router.message(Command("regions"))
async def get_all_regions_command(
        message: Message,
        region_service: RegionService,
        user_service: UserService,
        state: FSMContext
):
    await start_handler(
        message=message,
        user_service=user_service,
        state=state,
        region_service=region_service
    )
