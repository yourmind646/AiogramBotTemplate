# Aiogram
import aiogram.types as types
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram import Router, F

# DB
from database.orm import ORM as orm

# States
from states.main_states import AdminStates

# Init
admin_statistic_router = Router()


@admin_statistic_router.message(F.text == "📊 Статистика", StateFilter(AdminStates.main))
async def process_statistic(message: types.Message, state: FSMContext):

	all_users = await orm.get_all_users()

	msg_text = f"""<i>📊 Статистика</i>

🔹 Кол-во пользователей в боте: {len(all_users)} чел."""

	await message.answer(
		text = msg_text
	)
