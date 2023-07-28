# Aiogram imports
from aiogram import Dispatcher, filters, types
from aiogram.types.message import ParseMode
from aiogram.dispatcher import FSMContext


# loader
def load_start_handler(dispatcher: Dispatcher):

	# init
	global g_bot
	g_bot = dispatcher.bot

	# Register handlers
	dispatcher.register_message_handler(
		process_start,
		filters.CommandStart(),
		state = "*"
	)


async def process_start(message: types.Message, state: FSMContext):

	# close previous state
	await state.finish()

	# Get user data
	user_id = message.from_user.id
	user_fullname = message.from_user.full_name
	user_username = "@" + message.from_user.username if message.from_user.username is not None else "-"

	# hello msg
	hello_text = f"👋 Привет, {user_fullname} ({user_username})! Твой ID = {user_id}"

	await message.answer(
		text = hello_text
	)