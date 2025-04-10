from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config.config import Settings

def create_bot(config: Settings) -> tuple[Bot, Dispatcher]:
    bot = Bot(token=config.TG_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    return bot, dp