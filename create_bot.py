# aiogram
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder, StorageKey
from aiogram.types import BotCommand

# cfg
from decouple import config

# scheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# another
import logging


scheduler = AsyncIOScheduler(timezone = 'Europe/Moscow')

logging.basicConfig(level = logging.INFO, format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
redis_url = config('REDIS_URL')
bot = Bot(token = config('TOKEN'), default = DefaultBotProperties(parse_mode = ParseMode.HTML))
custom_prefix = config('REDIS_PREFIX')

storage = RedisStorage.from_url(redis_url)
storage.key_builder = DefaultKeyBuilder(prefix = custom_prefix)
dp = Dispatcher(storage = storage)

start_command = [BotCommand(command = "/start", description = "🔄 Перезапустить бота")]
