# Aiogram imports
from aiogram import Dispatcher, types, filters
from aiogram.dispatcher import FSMContext

# DB
from database.orm import ORM as orm

# States
from states.main_states import AdminStates


# loader
def load_admin_statistic_handler(dispatcher: Dispatcher):

	# init
	global g_bot
	g_bot = dispatcher.bot

	# Main handler
	dispatcher.register_message_handler(
		process_statistic,
		filters.Text(equals = "📊 Статистика"),
		state = AdminStates.main
	)


async def process_statistic(message: types.Message, state: FSMContext):

	all_users = await orm.get_all_users()

	msg_text = f"""<i>📊 Статистика</i>

🔹 Кол-во пользователей в боте: {len(all_users)} чел."""

	await message.answer(
		text = msg_text
	)
