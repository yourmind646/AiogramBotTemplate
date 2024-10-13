# Aiogram imports
import aiogram.types as types
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram import Router, F

# Bot
from create_bot import bot, storage, StorageKey

# Keyboards
from keyboards.admin_kbs import *

# DB
from database.orm import ORM as orm

# States
from states.main_states import AdminStates, AdminManagementStates

# Init
admin_management_router = Router()


@admin_management_router.message(F.text.in_(("👮‍♂️ Управление админами", "↩️ Назад")), StateFilter(AdminStates.main, AdminManagementStates))
async def add_admins_choose(message: types.Message, state: FSMContext):

	admins = await orm.get_all_admins()

	msg_text = "<i>👮‍♂️ Действующие администраторы</i>\n"

	for admin in admins:
		msg_text += f"- {admin.admin_user_id} | {admin.admin_username} | {admin.admin_fullname}\n"

	msg_text += f"\n<b>🔽 Выберите действие:</b>"

	await message.answer(
		text = msg_text,
		reply_markup = get_add_admins_kb()
	)

	await state.set_state(AdminManagementStates.main)


@admin_management_router.message(
	F.text == "➕ Добавить",
	StateFilter(AdminManagementStates.main))
async def add_admins_ADD_1(message: types.Message, state: FSMContext):

	msg_text = f"""Введите ID нового админа:"""

	await message.answer(
		text = msg_text,
		reply_markup = get_add_admins_back_kb()
	)

	await state.set_state(AdminManagementStates.add_admin)


@admin_management_router.message(
	F.text,
	StateFilter(AdminManagementStates.add_admin))
async def add_admins_ADD_2(message: types.Message, state: FSMContext):

	# validation
	if not message.text.isdigit():
		await message.answer(
			text = "⛔️ Только цифры! Повторите попытку:"
		)

		return

	admin_id = int(message.text)

	if not await orm.is_user_exists(admin_id):
		await message.answer(
			text = "⛔️ Пользователь не существует в БД! Повторите попытку:"
		)

		return
	
	new_admin = await orm.get_user(admin_id)

	await orm.create_admin_if_not_exists(new_admin.user_id, new_admin.username, new_admin.fullname)

	await state.clear()

	await message.answer("✅ Успешно")

	await add_admins_choose(message, state)


@admin_management_router.message(
	F.text == "➖ Убрать",
	StateFilter(AdminManagementStates.main))
async def add_admins_DEL_1(message: types.Message, state: FSMContext):

	msg_text = f"""Введите ID админа для удаления:"""

	await message.answer(
		text = msg_text,
		reply_markup = get_add_admins_back_kb()
	)

	await state.set_state(AdminManagementStates.del_admin)


@admin_management_router.message(
	F.text,
	StateFilter(AdminManagementStates.del_admin))
async def add_admins_DEL_2(message: types.Message, state: FSMContext):

	# validation
	if not message.text.isdigit():
		await message.answer(
			text = "⛔️ Только цифры! Повторите попытку:"
		)
		return

	admin_id = int(message.text)

	if not await orm.is_user_exists(admin_id):
		await message.answer(
			text = "⛔️ Пользователь не существует в БД! Повторите попытку:"
		)

		return
	
	# change admin state
	try:
		await bot.send_message(
			chat_id = admin_id,
			text = "☹️ Вы больше не являетесь админом!",
			reply_markup = ReplyKeyboardRemove()
		)
	except:
		pass

	await storage.set_state(key = StorageKey(bot_id = bot.id, chat_id = admin_id, user_id = admin_id), state = None)

	try:
		await orm.del_admin(admin_id)

		await message.answer("✅ Успешно")
	except:
		await message.answer("⛔️ Ошибка!")

	await add_admins_choose(message, state)
