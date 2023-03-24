# Aiogram imports
from aiogram import Dispatcher
from aiogram.types import Update
from aiogram.utils.exceptions import TelegramAPIError, RetryAfter, NetworkError, BadRequest
from aiohttp.client_exceptions import ServerDisconnectedError, ClientOSError, ClientConnectorError, ClientConnectionError

# Another imports
import logging

# init logging
logging.basicConfig(
		level = logging.INFO,
		format = u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
	)


# loader
def load_errors_handler(dispatcher: Dispatcher):

	dispatcher.register_errors_handler(process_errors)


# error handler
async def process_errors(update: Update, exception):

	if isinstance(exception, TelegramAPIError):
		logging.error(msg = f"TelegramAPIError - {exception}\n| {update}")
		return True

	if isinstance(exception, RetryAfter):
		logging.error(msg = f"RetryAfter - {exception}\n| {update}")
		return True

	if isinstance(exception, NetworkError):
		logging.error(msg = f"NetworkError - {exception}\n| {update}")
		return True

	if isinstance(exception, BadRequest):
		logging.error(msg = f"BadRequest - {exception}\n| {update}")
		return True
	# aiohttp
	if isinstance(exception, ServerDisconnectedError):
		logging.error(msg = f"ServerDisconnectedError - {exception}\n| {update}")
		return True

	if isinstance(exception, ClientOSError):
		logging.error(msg = f"ClientOSError - {exception}\n| {update}")
		return True

	if isinstance(exception, ClientConnectorError):
		logging.error(msg = f"ClientConnectorError - {exception}\n| {update}")
		return True

	if isinstance(exception, ClientConnectionError):
		logging.error(msg = f"ClientConnectionError - {exception}\n| {update}")
		return True

	logging.error(msg = f"Unknown Error - {exception}\n| {update}")
	return True