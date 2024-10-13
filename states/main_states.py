# Aiogram imports
from aiogram.fsm.state import State, StatesGroup


class MainStates(StatesGroup):

	main = State()


class AdminStates(StatesGroup):

	main = State()


class AdminMailerStates(StatesGroup):

	post = State()
	ikb = State()
	preview = State()


class AdminManagementStates(StatesGroup):

	main = State()

	add_admin = State()
	del_admin = State()