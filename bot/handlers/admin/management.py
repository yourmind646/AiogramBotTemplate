# Aiogram imports
import aiogram.types as types
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest

# Const
from create_bot import bot, storage, StorageKey, orm

# Keyboards
from keyboards.admin.main_kbs import *

# States
from states.admin_states import AdminStates, AdminManagementStates

# Config
from decouple import config

# Another
from contextlib import suppress


# Init
admin_management_router = Router()


@admin_management_router.message(F.text == "👮‍♂️ Управление админами", StateFilter(AdminStates.main))
@admin_management_router.message(F.text == "↩️ Назад", StateFilter(AdminManagementStates))
async def cmd_management(message: types.Message, state: FSMContext):

	admins = await orm.get_all_admins()

	msg_text = "<i>👮‍♂️ Действующие администраторы</i>\n"

	for admin in admins:
		msg_text += f"✦ [<code>{admin.user_id}</code>]: {admin.username if admin.username else admin.fullname}\n"

	msg_text += f"\n<b>🔽 Выберите действие:</b>"

	await message.answer(
		text = msg_text,
		reply_markup = get_add_admins_kb()
	)

	await state.set_state(AdminManagementStates.main)


#*############################
#*#           ADD            #
#*############################


@admin_management_router.message(F.text == "➕ Добавить", StateFilter(AdminManagementStates.main))
async def cmd_management_add_id(message: types.Message, state: FSMContext):

	msg_text = "➕ Введите User ID нового админа:"

	await message.answer(
		text = msg_text,
		reply_markup = get_back_kb()
	)

	await state.set_state(AdminManagementStates.add_admin)


@admin_management_router.message(F.text, StateFilter(AdminManagementStates.add_admin))
async def cmd_management_add_finish(message: types.Message, state: FSMContext):

	# validation
	if not message.text.isdigit():
		await message.answer(
			text = "⛔️ Только цифры! Повторите попытку:",
			reply_markup = get_back_kb()
		)
		return

	user_id = int(message.text)

	if not await orm.is_user_exists(user_id):
		await message.answer(
			text = "⛔️ Пользователь не существует в БД! Повторите попытку:",
			reply_markup = get_back_kb()
		)
		return
	
	user = await orm.get_user(user_id)
	await orm.create_admin(user.user_id, user.username, user.fullname)
	await message.answer("✅ Успешно!")
	await cmd_management(message, state)


#*############################
#*#          DELETE          #
#*############################


@admin_management_router.message(F.text == "➖ Удалить", StateFilter(AdminManagementStates.main))
async def cmd_management_delete(message: types.Message, state: FSMContext):

	msg_text = "➖ Введите ID админа для удаления:"

	await message.answer(
		text = msg_text,
		reply_markup = get_back_kb()
	)

	await state.set_state(AdminManagementStates.del_admin)


@admin_management_router.message(F.text, StateFilter(AdminManagementStates.del_admin))
async def cmd_management_delete_finish(message: types.Message, state: FSMContext):

	# validation
	if not message.text.isdigit():
		await message.answer(
			text = "⛔️ Только цифры! Повторите попытку:"
		)
		return

	user_id = int(message.text)

	if user_id == int(config("BASE_ADMIN")):
		await message.answer(
			text = "⛔️ Отказано! Повторите попытку:",
			reply_markup = get_back_kb()
		)
		return

	if not await orm.is_admin_exists(user_id):
		await message.answer(
			text = "⛔️ Админ не найден! Повторите попытку:"
		)
		return
	
	# change admin state
	with suppress(TelegramBadRequest):
		await bot.send_message(
			chat_id = user_id,
			text = "☹️ Вы больше не являетесь админом!",
			reply_markup = types.ReplyKeyboardRemove()
		)

	await storage.set_state(key = StorageKey(bot_id = bot.id, chat_id = user_id, user_id = user_id), state = None)
	await orm.delete_admin(user_id)
	await message.answer("✅ Успешно!")
	await cmd_management(message, state)
