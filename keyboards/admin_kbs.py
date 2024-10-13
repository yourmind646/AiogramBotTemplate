# Aiogram imports
from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton
from aiogram.types import ReplyKeyboardRemove


def get_main_menu_kb():

	builder = ReplyKeyboardBuilder()

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

	builder.add(
		statistic_btn, mailer_btn,
		users_list, admin_management_btn,
		exit_btn
	)

	builder.adjust(2)

	return builder.as_markup(resize_keyboard = True, is_persistent = True)


def get_add_admins_kb():

	builder = ReplyKeyboardBuilder()

	add_btn = KeyboardButton(
		text = "➕ Добавить"
	)

	remove_btn = KeyboardButton(
		text = "➖ Убрать"
	)

	back_btn = KeyboardButton(
		text = "↩️ Вернуться в меню"
	)

	builder.add(add_btn, remove_btn, back_btn)
	builder.adjust(2)

	return builder.as_markup(resize_keyboard = True, is_persistent = True)


def get_add_admins_back_kb():

	builder = ReplyKeyboardBuilder()

	back_btn = KeyboardButton(
		text = "↩️ Назад"
	)

	builder.add(back_btn)

	return builder.as_markup(
		row_width = 1,
		resize_keyboard = True
	)
