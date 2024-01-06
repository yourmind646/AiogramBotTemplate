# Aiogram imports
from aiogram import Dispatcher, filters, types
from aiogram.dispatcher import FSMContext

# Database
from database.orm import ORM as orm

# States
from states.main_states import MainStates

# Modules
from modules.to_html import to_html

# Another
from datetime import datetime


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
	await state.reset_state()

	# Get user data
	user_id = message.from_user.id
	username = "@" + message.from_user.username if message.from_user.username is not None else "-"
	fullname = to_html(message.from_user.full_name)
	
	# Create row
	await orm.create_user_if_not_exists(
		user_id = user_id,
		username = username,
		fullname = fullname,
		register_date = datetime.utcnow()
	)

	# hello msg
	hello_text = f"👋 Привет, {fullname} ({username})! Твой ID = {user_id}"

	await message.answer(
		text = hello_text
	)

	# set main states
	await MainStates.main.set()
