# Aiogram
import aiogram.types as types
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram import Router, F

# Const
from create_bot import orm

# States
from states.admin_states import AdminStates

# Init
admin_statistic_router = Router()


@admin_statistic_router.message(F.text == "📊 Статистика", StateFilter(AdminStates.main))
async def cmd_statistic(message: types.Message, state: FSMContext):

	users_count = await orm.get_users_count()

	msg_text = f"""<i>📊 Статистика</i>

🔹 Кол-во пользователей в боте: {users_count:,} чел."""

	await message.answer(text = msg_text)
