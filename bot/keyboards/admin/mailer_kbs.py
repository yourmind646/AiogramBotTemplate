# Aiogram imports
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, KeyboardButton


def get_back_to_main_kb():

	builder = ReplyKeyboardBuilder()

	builder.row(
		KeyboardButton(text = "↩️ Вернуться в меню")
	)

	return builder.as_markup(resize_keyboard = True)


def get_back_kb():

	builder = ReplyKeyboardBuilder()

	builder.row(
		KeyboardButton(text = "↩️ Назад")
	)

	return builder.as_markup(resize_keyboard = True)


def get_skip_kb():

	builder = ReplyKeyboardBuilder()

	builder.add(
		KeyboardButton(text = "↪️ Пропустить"),
		KeyboardButton(text = "↩️ Назад")
	)
	builder.adjust(1)

	return builder.as_markup(resize_keyboard = True)


def get_mailer_finish_kb():

	builder = ReplyKeyboardBuilder()

	builder.add(
		KeyboardButton(text = "🟢 Начать рассылку"),
		KeyboardButton(text = "↩️ Назад")
	)
	builder.adjust(1)

	return builder.as_markup(resize_keyboard = True, is_persistent = True)


def get_mailer_btn_ikb(buttons_preset: list[str]|None):

	builder = InlineKeyboardBuilder()

	if buttons_preset:
		for row in buttons_preset:
			for btn_name, btn_url in row:
				builder.row(InlineKeyboardButton(text = btn_name, url = btn_url))

	return builder.as_markup()
