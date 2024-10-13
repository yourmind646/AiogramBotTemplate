# Aiogram imports
import aiogram.types as types
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram import Router, F

# Bot
from create_bot import bot

# Keyboards
from keyboards.admin_mailer_kbs import *

# DB
from database.orm import ORM as orm

# States
from states.main_states import AdminStates, AdminMailerStates

# Funcs
from handlers.admin.main import show_admin_menu

admin_mailer_router = Router()


@admin_mailer_router.message(F.text == "✉️ Рассылка", StateFilter(AdminStates.main))
@admin_mailer_router.message(F.text == "↩️ Назад", StateFilter(AdminMailerStates))
async def process_mailer_post(message: types.Message, state: FSMContext):

	msg_text = "✉️ Отправьте пост одним сообщением:"

	await message.answer(
		text = msg_text,
		reply_markup = get_back_to_main_kb()
	)

	await state.set_state(AdminMailerStates.post)


@admin_mailer_router.message(StateFilter(AdminMailerStates.post))
async def process_mailer_ikb(message: types.Message, state: FSMContext):

	await state.update_data(admin_mailer_post = message.message_id)

	msg_text = "✉️ Введите кнопки в формате <b>НАЗВАНИЕ + ССЫЛКА</b>:"

	await message.answer(
		text = msg_text,
		reply_markup = get_skip_kb()
	)

	await state.set_state(AdminMailerStates.ikb)


@admin_mailer_router.message(F.text, StateFilter(AdminMailerStates.ikb))
async def process_mailer_preview(message: types.Message, state: FSMContext):

	ikb = message.text.split("\n") if message.text != "↪️ Пропустить" else None
	await state.update_data(admin_mailer_ikb = ikb)

	state_data = await state.get_data()
	post = state_data.get("admin_mailer_post")

	await message.answer(
		text = "✉️ Предпросмотр:",
		reply_markup = get_mailer_finish_kb()
	)

	try:
		await bot.copy_message(
			chat_id = message.from_user.id,
			from_chat_id = message.from_user.id,
			message_id = post,
			reply_markup = get_mailer_btn_ikb(buttons_preset = ikb)
		)
	except:
		await message.answer(
			text = "🔴 Ошибка!"
		)
		await process_mailer_post(message, state)
		return

	await state.set_state(AdminMailerStates.preview)


@admin_mailer_router.message(F.text == "🟢 Начать рассылку", StateFilter(AdminMailerStates.preview))
async def process_mailer_finish(message: types.Message, state: FSMContext):

	state_data = await state.get_data()
	ikb = state_data.get("admin_mailer_ikb")
	post = state_data.get("admin_mailer_post")
	
	all_users = await orm.get_all_users()

	# info
	await message.answer(
		text = "▶️✉️ Рассылка запущена..."
	)

	# reset mailer config
	await state.clear()

	# back to main menu
	await show_admin_menu(message, state)

	counter = 0
	for user in all_users:
		try:
			await bot.copy_message(
				chat_id = user.user_id,
				from_chat_id = message.from_user.id,
				message_id = post,
				reply_markup = get_mailer_btn_ikb(buttons_preset = ikb)
			)
			counter += 1
		except:
			pass

	await message.answer(
		text = f"✅ Рассылка завершена! Сообщение отправлено {counter}/{len(all_users)}."
	)
