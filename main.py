# Aiogram imports
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# Handlers
from handlers.errors import load_errors_handler
from handlers.start import load_start_handler

# My modules
from modules import cfg_loader

# Another imports
import asyncio

# Loading cfg
config = cfg_loader.load_config()

# Initialize bot object
bot = Bot(token = config["BOT_API_TOKEN"])
storage = MemoryStorage() # for FSM
dp = Dispatcher(bot, storage = storage)


if __name__ == "__main__":

	# Load errors handler
	load_errors_handler(
		dispatcher = dp
	)

	# Load handlers
	load_start_handler(
		bot = bot,
		dispatcher = dp
	)

	# Load handlers
	# load_admin_handler(
	# 	bot = bot,
	# 	dispatcher = dp
	# )

	# create loop
	loop = asyncio.new_event_loop()
	# set new loop
	asyncio.set_event_loop(loop = loop)
	# add task
	#loop.create_task(test())
	
	# Start long-polling
	executor.start_polling(dp, skip_updates = True)