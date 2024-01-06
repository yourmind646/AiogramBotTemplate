# Aiogram imports
from aiogram import Dispatcher, types, filters
from aiogram.types.message import ContentType
from aiogram.dispatcher import FSMContext

# Keyboards
from keyboards.admin_mailer_kbs import *

# DB
from database.orm import ORM as orm

# States
from states.main_states import AdminStates, AdminMailerStates

# Funcs
from handlers.admin.main import show_admin_menu


# loader
def load_admin_mailer_handler(dispatcher: Dispatcher):

	# init
	global g_bot
	g_bot = dispatcher.bot

	# Register handlers
	dispatcher.register_message_handler(
		process_mailer_menu,
		filters.Text(equals = ["✉️ Рассылка", "🔙 Назад"]),
		state = [
			AdminStates.main,
			
			AdminMailerStates.mailer_text_enter_text,
			AdminMailerStates.mailer_text_enter_link,
			AdminMailerStates.mailer_text_enter_finish,

			AdminMailerStates.mailer_image_enter_image,
			AdminMailerStates.mailer_image_enter_caption,
			AdminMailerStates.mailer_image_enter_link,
			AdminMailerStates.mailer_image_enter_finish
		]
	)

	## TEXT MAILER
	dispatcher.register_message_handler(
		process_mailer_text_1,
		filters.Text(equals = "📝 Текст"),
		state = AdminMailerStates.mailer_menu
	)

	dispatcher.register_message_handler(
		process_mailer_text_2,
		content_types = ContentType.TEXT,
		state = AdminMailerStates.mailer_text_enter_text
	)

	dispatcher.register_message_handler(
		process_mailer_text_3,
		content_types = ContentType.TEXT,
		state = AdminMailerStates.mailer_text_enter_link
	)

	dispatcher.register_message_handler(
		process_mailer_text_finish,
		filters.Text(equals = "🟢 Начать рассылку"),
		state = AdminMailerStates.mailer_text_enter_finish
	)

	## IMAGE MAILER
	dispatcher.register_message_handler(
		process_mailer_image_1,
		filters.Text(equals = "🖼 Фото"),
		state = AdminMailerStates.mailer_menu
	)

	dispatcher.register_message_handler(
		process_mailer_image_2,
		content_types = ContentType.PHOTO,
		state = AdminMailerStates.mailer_image_enter_image
	)

	dispatcher.register_message_handler(
		process_mailer_image_3,
		content_types = ContentType.TEXT,
		state = AdminMailerStates.mailer_image_enter_caption
	)

	dispatcher.register_message_handler(
		process_mailer_image_4,
		content_types = ContentType.TEXT,
		state = AdminMailerStates.mailer_image_enter_link
	)

	dispatcher.register_message_handler(
		process_mailer_image_finish,
		filters.Text(equals = "🟢 Начать рассылку"),
		state = AdminMailerStates.mailer_image_enter_finish
	)


async def process_mailer_menu(message: types.Message, state: FSMContext):

	msg_text = "Выберите тип рассылки:"

	await message.answer(
		text = msg_text,
		reply_markup = get_mailer_menu_kb()
	)

	await AdminMailerStates.mailer_menu.set()


### TEXT
async def process_mailer_text_1(message: types.Message, state: FSMContext):

	msg_text = "Введите текст рассылки:"

	await message.answer(
		text = msg_text,
		reply_markup = get_back_kb()
	)

	await AdminMailerStates.mailer_text_enter_text.set()


async def process_mailer_text_2(message: types.Message, state: FSMContext):

	async with state.proxy() as storage:
		storage["admin_mailer_text"] = message.html_text

	msg_text = "Введите кнопки в формате <b>НАЗВАНИЕ + ССЫЛКА</b>:"

	await message.answer(
		text = msg_text,
		reply_markup = get_skip_kb()
	)

	await AdminMailerStates.mailer_text_enter_link.set()


async def process_mailer_text_3(message: types.Message, state: FSMContext):

	async with state.proxy() as storage:
		storage["admin_mailer_link"] = message.text if message.text != "↪️ Пропустить" else None
		admin_mailer_text = storage.get("admin_mailer_text")
		admin_mailer_link = storage.get("admin_mailer_link")

	await message.answer(
		text = "👀 Предпросмотр:",
		reply_markup = get_mailer_finish_kb()
	)

	try:
		await message.answer(
			text = admin_mailer_text,
			reply_markup = get_mailer_btn_ikb(buttons_preset = admin_mailer_link)
		)
	except:
		await message.answer(
			text = "🔴 Ошибка!",
			reply_markup = get_mailer_menu_kb()
		)

		await AdminMailerStates.mailer_menu.set()
		return

	await AdminMailerStates.mailer_text_enter_finish.set()


async def process_mailer_text_finish(message: types.Message, state: FSMContext):

	# unpack
	async with state.proxy() as storage:
		text = storage.get("admin_mailer_text")
		link = storage.get("admin_mailer_link")

	all_users = await orm.get_all_users()

	# info
	await message.answer(
		text = "▶️ Рассылка запущена..."
	)

	# reset mailer config
	await state.reset_data()

	# back to main menu
	await show_admin_menu(message, state)

	counter = 0
	for user in all_users:
		try:
			await g_bot.send_message(
				chat_id = user.user_id,
				text = text,
				reply_markup = get_mailer_btn_ikb(buttons_preset = link)
			)

			counter += 1
		except Exception as e:
			pass

	await message.answer(
		text = f"✅ Рассылка завершена! Сообщение отправлено {counter}/{len(all_users)}."
	)


### IMAGE
async def process_mailer_image_1(message: types.Message, state: FSMContext):

	msg_text = "Отправьте картинку:"

	await message.answer(
		text = msg_text,
		reply_markup = get_back_kb()
	)

	await AdminMailerStates.mailer_image_enter_image.set()


async def process_mailer_image_2(message: types.Message, state: FSMContext):

	async with state.proxy() as storage:
		storage["admin_mailer_image"] = message.photo[-1].file_id

	msg_text = "Введите описание к фото:"

	await message.answer(
		text = msg_text,
		reply_markup = get_skip_kb()
	)

	await AdminMailerStates.mailer_image_enter_caption.set()


async def process_mailer_image_3(message: types.Message, state: FSMContext):

	# validation
	if len(message.text) > 1024:
		await message.answer("🔴 Допустимый лимит символов - 1024. Повторите попытку:")
		return

	async with state.proxy() as storage:
		storage["admin_mailer_caption"] = message.html_text if message.text != "↪️ Пропустить" else None

	msg_text = "Введите кнопки в формате <b>НАЗВАНИЕ + ССЫЛКА</b>:"

	await message.answer(
		text = msg_text,
		reply_markup = get_skip_kb()
	)

	await AdminMailerStates.mailer_image_enter_link.set()


async def process_mailer_image_4(message: types.Message, state: FSMContext):

	async with state.proxy() as storage:
		storage["admin_mailer_link"] = message.text if message.text != "↪️ Пропустить" else None
		admin_mailer_link = storage.get("admin_mailer_link")
		caption = storage.get("admin_mailer_caption")
		photo = storage.get("admin_mailer_image")

	await message.answer(
		text = "👀 Предпросмотр:",
		reply_markup = get_mailer_finish_kb()
	)

	try:
		await message.answer_photo(
			photo = photo,
			caption = caption,
			reply_markup = get_mailer_btn_ikb(buttons_preset = admin_mailer_link)
		)
	except Exception as e:
		await message.answer(
			text = "🔴 Ошибка!",
			reply_markup = get_mailer_menu_kb()
		)

		await AdminMailerStates.mailer_menu.set()
		return

	await AdminMailerStates.mailer_image_enter_finish.set()


async def process_mailer_image_finish(message: types.Message, state: FSMContext):

	# unpack
	async with state.proxy() as storage:
		caption = storage.get("admin_mailer_caption")
		photo = storage.get("admin_mailer_image")
		link = storage.get("admin_mailer_link")

	all_users = await orm.get_all_users()

	# info
	await message.answer(
		text = "▶️ Рассылка запущена..."
	)

	# reset mailer config
	await state.reset_data()

	# back to main menu
	await show_admin_menu(message, state)

	counter = 0
	for user in all_users:
		try:
			await g_bot.send_photo(
				chat_id = user.user_id,
				photo = photo,
				caption = caption,
				reply_markup = get_mailer_btn_ikb(buttons_preset = link)
			)

			counter += 1
		except:
			pass

	await message.answer(
		text = f"✅ Рассылка завершена! Сообщение отправлено {counter}/{len(all_users)}."
	)