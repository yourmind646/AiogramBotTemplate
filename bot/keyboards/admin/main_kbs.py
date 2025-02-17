# Aiogram imports
from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton, InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton


def get_main_menu_kb():

	builder = ReplyKeyboardBuilder()

	builder.row(
		KeyboardButton(text = "📊 Статистика"),
		KeyboardButton(text = "✉️ Рассылка")
	)

	builder.row(
		KeyboardButton(text = "🚫 Черный список"),
		KeyboardButton(text = "⚙️ Настройки")
	)

	builder.row(
		KeyboardButton(text = "📑 Список пользователей"),
		KeyboardButton(text = "👮‍♂️ Управление админами")
	)

	builder.row(
		KeyboardButton(text = "🔚 Выйти")
	)

	return builder.as_markup(resize_keyboard = True, is_persistent = True)


def get_add_admins_kb():

	builder = ReplyKeyboardBuilder()

	builder.row(
		KeyboardButton(text = "➕ Добавить"),
		KeyboardButton(text = "➖ Удалить")
	)

	builder.row(
		KeyboardButton(text = "↩️ Вернуться в меню")
	)

	return builder.as_markup(resize_keyboard = True, is_persistent = True)


def get_back_kb():

	builder = ReplyKeyboardBuilder()

	builder.row(
		KeyboardButton(text = "↩️ Назад")
	)

	return builder.as_markup(resize_keyboard = True)


def get_settings_kb() -> ReplyKeyboardMarkup:

	builder = ReplyKeyboardBuilder()

	builder.add(
		KeyboardButton(text = "↩️ Вернуться в меню")
	)
	builder.adjust(2)

	return builder.as_markup(resize_keyboard = True, is_persistent = True)


def get_blacklist_kb():

	builder = ReplyKeyboardBuilder()

	builder.row(
		KeyboardButton(text = "👁 Открыть список")
	)

	builder.row(
		KeyboardButton(text = "➕ Добавить"),
		KeyboardButton(text = "➖ Удалить")
	)

	builder.row(
		KeyboardButton(text = "↩️ Вернуться в меню")
	)

	return builder.as_markup(resize_keyboard = True, is_persistent = True)


def get_bookList_ikb(prefix: str, offset: int, max_offset: int, items: list[tuple], element_col: int = 10) -> InlineKeyboardMarkup:
	
	builder = InlineKeyboardBuilder()

	for item_id, item_name in items[offset * element_col:(offset + 1) * element_col]:
		builder.row(InlineKeyboardButton(text = f"{item_name}", callback_data = f"{prefix}_pick_{item_id}"))

	builder.row(
		InlineKeyboardButton(text = "⬅️", callback_data = f"{prefix}_prev"),
		InlineKeyboardButton(text = "➡️", callback_data = f"{prefix}_next")
	)

	return builder.as_markup()
