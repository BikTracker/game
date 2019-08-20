import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

try:
    import Local_Config as config
except ImportError:
    import Example_Config as config


logging.basicConfig(level=logging.DEBUG)

bot = Bot(config.BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
