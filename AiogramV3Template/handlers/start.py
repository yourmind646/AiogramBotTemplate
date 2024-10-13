# Aiogram
import aiogram.types as types
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, StateFilter
from aiogram import Router, F

# Utils
from utils.to_html import to_html

# Database
from database.orm import ORM as orm

# States
from states.main_states import MainStates

# Another
from datetime import datetime

# Init
start_router = Router()


@start_router.message(CommandStart(), StateFilter("*"))
async def cmd_start(message: types.Message, state: FSMContext):

	# close previous state
	await state.clear()

	# Get user data
	user_id = message.from_user.id
	username = "@" + message.from_user.username if message.from_user.username is not None else "-"
	fullname = to_html(message.from_user.full_name)
	
	# Create row
	await orm.create_user_if_not_exists(
		user_id = user_id,
		username = username,
		fullname = fullname,
		register_date = datetime.now()
	)

	# hello msg
	hello_text = f"👋 Привет, {fullname} ({username})! Твой ID = {user_id}"

	await message.answer(
		text = hello_text
	)

	# set main states
	await state.set_state(MainStates.main)
