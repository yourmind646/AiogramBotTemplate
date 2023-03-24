# Aiogram imports
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.redis import RedisStorage2

# Handlers
from handlers.start import load_start_handler

# My modules
from modules import cfg_loader

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
bot = Bot(token = config["BOT_API_TOKEN"])
storage = RedisStorage2("127.0.0.1", 6379, db = 5, pool_size = 10, prefix = "proj") # for FSM
dp = Dispatcher(bot, storage = storage)


if __name__ == "__main__":

	# Load handlers
	load_start_handler(
		dispatcher = dp
	)

	# create loop
	loop = asyncio.new_event_loop()
	# set new loop
	asyncio.set_event_loop(loop = loop)
	# add task
	#loop.create_task(test())
	
	# Start long-polling
	executor.start_polling(dp, skip_updates = False)
