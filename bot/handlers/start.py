# Aiogram
import aiogram.types as types
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, StateFilter
from aiogram import Router, F

# Utils
from utils.text_tools import to_html

# Const
from create_bot import orm

# States
from states.client_states import MainStates

# Another
from datetime import datetime, timezone


# Init
start_router = Router()


@start_router.message(CommandStart(), StateFilter("*"))
async def cmd_start(message: types.Message, state: FSMContext):

	if message.chat.type != "private":
		return

	user_id = message.from_user.id
	username = "@" + message.from_user.username if message.from_user.username is not None else None
	fullname = to_html(message.from_user.full_name)
	
	await orm.create_user(
		user_id = user_id,
		username = username,
		fullname = fullname,
		register_date = datetime.now(timezone.utc)
	)

	msg_text = f"👋 Привет, {fullname} ({username})! Твой ID = <code>{user_id}</code>"

	await message.answer(
		text = msg_text,
		reply_markup = types.ReplyKeyboardRemove()
	)

	await state.set_state(MainStates.main)
