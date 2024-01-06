# Aiogram imports
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_main_menu_kb():

	reply_markup = ReplyKeyboardMarkup(
		resize_keyboard = True,
		is_persistent = True,
		row_width = 2
	)

	statistic_btn = KeyboardButton(
		text = "📊 Статистика"
	)

	mailer_btn = KeyboardButton(
		text = "✉️ Рассылка"
	)

	users_list = KeyboardButton(
		text = "📑 Список пользователей"
	)

	admin_management_btn = KeyboardButton(
		text = "👮‍♂️ Управление админами"
	)

	exit_btn = KeyboardButton(
		text = "🔚 Выйти"
	)

	reply_markup.add(statistic_btn, admin_management_btn, mailer_btn, users_list)
	reply_markup.row(exit_btn)

	return reply_markup


def get_add_admins_kb():

	reply_markup = ReplyKeyboardMarkup(
		row_width = 2,
		resize_keyboard = True,
		is_persistent = True
	)

	_1 = KeyboardButton(
		text = "➕ Добавить"
	)

	_2 = KeyboardButton(
		text = "➖ Убрать"
	)

	exit_btn = KeyboardButton(
		text = "🔙 Вернуться в меню"
	)

	reply_markup.add(_1, _2, exit_btn)

	return reply_markup


def get_add_admins_back_kb():

	reply_markup = ReplyKeyboardMarkup(
		row_width = 1,
		resize_keyboard = True
	)

	back_btn = KeyboardButton(
		text = "🔙 Назад"
	)

	reply_markup.add(back_btn)

	return reply_markup
