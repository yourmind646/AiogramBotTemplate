# Aiogram imports
from aiogram import Dispatcher, types, filters
from aiogram.dispatcher import FSMContext

# Keyboards
from keyboards.admin_kbs import *

# Database
from database.orm import ORM as orm

# States
from states.main_states import AdminStates, AdminMailerStates, AdminManagementStates

# Funcs
from handlers.start import process_start


# loader
def load_admin_main_handler(dispatcher: Dispatcher):

	# init
	global g_bot
	g_bot = dispatcher.bot

	# Main handler
	dispatcher.register_message_handler(
		process_login_as_admin,
		filters.Command("admin"),
		state = "*"
	)

	## Exit handler
	dispatcher.register_message_handler(
		process_admin_exit,
		filters.Text(equals = "🔚 Выйти"),
		state = AdminStates.main
	)
	###

	## SHOW MAIN MENU
	dispatcher.register_message_handler(
		show_admin_menu,
		filters.Text(equals = ["🔙 Вернуться в меню"]),
		state = [
			AdminMailerStates.mailer_menu,
			AdminManagementStates.main
		]
	)
	###


async def process_login_as_admin(message: types.Message, state: FSMContext):

	await message.delete()

	# admin check
	is_admin_exists = await orm.is_admin_exists(admin_user_id = message.from_user.id)

	if is_admin_exists:
		await show_admin_menu(message, state)
	else:
		await message.answer(
			text = "🤨"
		)


async def process_admin_exit(message: types.Message, state: FSMContext):

	await message.answer(
		text = "🔴.",
		reply_markup = ReplyKeyboardRemove()
	)

	await process_start(message, state)


async def show_admin_menu(message: types.Message, state: FSMContext):

	msg_text = "👮‍♂️ Вы находитесь в админ-панели"

	await message.answer(
		text = msg_text,
		reply_markup = get_main_menu_kb()
	)

	await AdminStates.main.set()
