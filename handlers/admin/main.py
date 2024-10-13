# Aiogram
import aiogram.types as types
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram import Router, F

# Keyboards
from keyboards.admin_kbs import *

# Database
from database.orm import ORM as orm

# States
from states.main_states import AdminStates, AdminMailerStates, AdminManagementStates

# Funcs
from handlers.start import cmd_start

# Init
admin_main_router = Router()


@admin_main_router.message(Command("admin"), StateFilter("*"))
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


@admin_main_router.message(F.text == "🔚 Выйти", StateFilter(AdminStates.main))
async def process_admin_exit(message: types.Message, state: FSMContext):

	await message.answer(
		text = "🔴.",
		reply_markup = ReplyKeyboardRemove()
	)

	await cmd_start(message, state)


@admin_main_router.message(F.text == "↩️ Вернуться в меню", StateFilter(AdminManagementStates.main, AdminMailerStates.post))
async def show_admin_menu(message: types.Message, state: FSMContext):

	msg_text = "👮‍♂️ Вы находитесь в админ-панели"

	await message.answer(
		text = msg_text,
		reply_markup = get_main_menu_kb()
	)

	await state.set_state(AdminStates.main)
