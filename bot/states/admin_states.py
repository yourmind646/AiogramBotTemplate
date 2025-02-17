# Aiogram imports
from aiogram.fsm.state import State, StatesGroup


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


class AdminSettingsStates(StatesGroup):

	main = State()
	edit_photo = State()


class AdminBlacklistStates(StatesGroup):

	main = State()

	add_blacklist = State()
	del_blacklist = State()
