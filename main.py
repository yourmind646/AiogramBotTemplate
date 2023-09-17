# Aiogram imports
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.types import BotCommand

# Handlers
from handlers.start import load_start_handler

# Admin handlers
from handlers.admin.main import load_admin_main_handler
from handlers.admin.list_of_users import load_admin_list_of_users_handler
from handlers.admin.mailer import load_admin_mailer_handler
from handlers.admin.statistic import load_admin_statistic_handler
from handlers.admin.management import load_admin_management_handler

# My modules
from modules import cfg_loader

# ORM
from database.orm import ORM as orm

# Another imports
import asyncio
import logging


# init logging
logging.basicConfig(
	level = logging.INFO,
	format = u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
)

# Loading cfg
config = cfg_loader.load_config()

# Initialize bot object
bot = Bot(token = config.get("BOT_API_TOKEN"))
bot.parse_mode = "html"

storage = RedisStorage2("127.0.0.1", 6379, db = 5, pool_size = 10, prefix = "proj_name")
dp = Dispatcher(bot, storage = storage)
start_command = [BotCommand(command = "/start", description = "🔄 Перезапустить бота")]


if __name__ == "__main__":

	# create loop
	loop = asyncio.new_event_loop()
	# set new loop
	asyncio.set_event_loop(loop = loop)

	# Load handlers
	load_start_handler(
		dispatcher = dp
	)

	# Admins handlers
	load_admin_main_handler(
		dispatcher = dp
	)

	load_admin_statistic_handler(
		dispatcher = dp
	)

	load_admin_list_of_users_handler(
		dispatcher = dp
	)

	load_admin_mailer_handler(
		dispatcher = dp
	)

	load_admin_management_handler(
		dispatcher = dp
	)
	
	loop.create_task(orm.proceed_schemas())
	loop.create_task(bot.set_my_commands(start_command))
	loop.create_task(orm.create_admin_if_not_exists(872114089, "@RubyHunter", "ruby"))

	# Start long-polling
	executor.start_polling(dp, skip_updates = False)
