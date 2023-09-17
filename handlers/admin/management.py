# Aiogram imports
from aiogram import Dispatcher, types, filters
from aiogram.types.message import ParseMode, ContentType
from aiogram.dispatcher import FSMContext

# Keyboards
from keyboards.admin_kbs import *

# DB
from database.orm import ORM as orm

# States
from states.main_states import AdminStates, AdminManagementStates


# loader
def load_admin_management_handler(dispatcher: Dispatcher):

	# init
	global g_bot, g_storage
	g_bot = dispatcher.bot
	g_storage = dispatcher.storage
	
	dispatcher.register_message_handler(
		add_admins_choose,
		filters.Text(equals = ["👮‍♂️ Управление админами", "🔙 Назад"]),
		state = [AdminStates.main, AdminManagementStates.add_admin, AdminManagementStates.del_admin]
	)

	## ADD ADMIN
	dispatcher.register_message_handler(
		add_admins_ADD_1,
		filters.Text(equals = ["➕ Добавить"]),
		state = AdminManagementStates.main
	)

	dispatcher.register_message_handler(
		add_admins_ADD_2,
		content_types = ContentType.TEXT,
		state = AdminManagementStates.add_admin
	)

	## DEL ADMIN
	dispatcher.register_message_handler(
		add_admins_DEL_1,
		filters.Text(equals = ["➖ Убрать"]),
		state = AdminManagementStates.main
	)

	dispatcher.register_message_handler(
		add_admins_DEL_2,
		content_types = ContentType.TEXT,
		state = AdminManagementStates.del_admin
	)


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

	await AdminManagementStates.main.set()


async def add_admins_ADD_1(message: types.Message, state: FSMContext):

	msg_text = f"""Введите ID нового админа:"""

	await message.answer(
		text = msg_text,
		reply_markup = get_add_admins_back_kb()
	)

	await AdminManagementStates.add_admin.set()


async def add_admins_ADD_2(message: types.Message, state: FSMContext):

	# validation
	if not message.text.isdigit():
		await message.answer(
			text = "🔴 Только цифры! Повторите попытку:"
		)

		return

	admin_id = int(message.text)

	if not await orm.is_user_exists(admin_id):
		await message.answer(
			text = "🔴 Пользователь не существует в БД! Повторите попытку:"
		)

		return
	
	new_admin = await orm.get_user(admin_id)

	await orm.create_admin_if_not_exists(new_admin.user_id, new_admin.username, new_admin.fullname)

	await state.reset_data()

	await message.answer("✅ Успешно")

	await add_admins_choose(message, state)


async def add_admins_DEL_1(message: types.Message, state: FSMContext):

	msg_text = f"""Введите ID админа для удаления:"""

	await message.answer(
		text = msg_text,
		parse_mode = ParseMode.HTML,
		reply_markup = get_add_admins_back_kb()
	)

	await AdminManagementStates.del_admin.set()


async def add_admins_DEL_2(message: types.Message, state: FSMContext):

	# validation
	if not message.text.isdigit():
		await message.answer(
			text = "🔴 Только цифры! Повторите попытку:"
		)

		return

	admin_id = int(message.text)

	if not await orm.is_user_exists(admin_id):
		await message.answer(
			text = "🔴 Пользователь не существует в БД! Повторите попытку:"
		)

		return
	
	# change admin state
	try:
		await g_bot.send_message(
			chat_id = admin_id,
			text = "☹️ Вы больше не являетесь админом!",
			reply_markup = ReplyKeyboardRemove()
		)
	except:
		pass

	try:
		await FSMContext(g_storage, admin_id, admin_id).set_state(None)
	except:
		pass

	try:
		await orm.del_admin(admin_id)

		await message.answer("✅ Успешно")
	except Exception as e:
		await message.answer("🔴 Ошибка!")

	await add_admins_choose(message, state)