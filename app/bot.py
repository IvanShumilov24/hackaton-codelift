from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

from config.config import Settings


async def create_bot(config: Settings) -> tuple[Bot, Dispatcher]:
    bot: Bot = Bot(token=config.TG_TOKEN)
    user_commands = [
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="regions", description="Просмотреть список регионов")
    ]
    await bot.set_my_commands(user_commands)
    dp = Dispatcher(storage=MemoryStorage())
    return bot, dp
