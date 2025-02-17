# Aiogram
import aiogram.types as types
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram import Router, F

# Const
from create_bot import orm

# Keyboards
from keyboards.admin.main_kbs import *

# States
from states.admin_states import (
	AdminStates, AdminMailerStates, AdminManagementStates,
	AdminSettingsStates, AdminBlacklistStates
)

# Funcs
from handlers.start import cmd_start


# Init
admin_main_router = Router()


@admin_main_router.message(Command("admin"), StateFilter("*"))
async def cmd_login_as_admin(message: types.Message, state: FSMContext):

	if message.chat.type != "private":
		return

	is_admin_exists = await orm.is_admin_exists(user_id = message.from_user.id)

	if is_admin_exists:
		await show_admin_menu(message, state)
	else:
		await message.answer(text = "🤨")


@admin_main_router.message(F.text == "🔚 Выйти", StateFilter(AdminStates.main))
async def cmd_admin_exit(message: types.Message, state: FSMContext):

	await message.answer(
		text = "🚪⠀",
		reply_markup = types.ReplyKeyboardRemove()
	)

	await cmd_start(message, state)


@admin_main_router.message(F.text == "↩️ Вернуться в меню", StateFilter(
	AdminManagementStates.main, AdminMailerStates.post,
	AdminSettingsStates.main, AdminBlacklistStates.main
))
async def show_admin_menu(message: types.Message, state: FSMContext):

	msg_text = "👮‍♂️ Вы находитесь в админ-панели"

	await message.answer(
		text = msg_text,
		reply_markup = get_main_menu_kb()
	)

	await state.set_state(AdminStates.main)
