# Aiogram imports
from aiogram.dispatcher.filters.state import State, StatesGroup


class MainStates(StatesGroup):

	main = State()


class AdminStates(StatesGroup):

	main = State()


class AdminMailerStates(StatesGroup):

	mailer_menu = State()

	mailer_text_enter_text = State()
	mailer_text_enter_link = State()
	mailer_text_enter_finish = State()

	mailer_image_enter_image = State()
	mailer_image_enter_caption = State()
	mailer_image_enter_link = State()
	mailer_image_enter_finish = State()


class AdminManagementStates(StatesGroup):

	main = State()

	add_admin = State()
	del_admin = State()