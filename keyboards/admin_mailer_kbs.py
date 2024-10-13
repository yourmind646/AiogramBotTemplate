# Aiogram imports
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, KeyboardButton


def get_back_to_main_kb():

	builder = ReplyKeyboardBuilder()

	exit_btn = KeyboardButton(
		text = "↩️ Вернуться в меню"
	)

	builder.add(exit_btn)

	return builder.as_markup(resize_keyboard = True, is_persistent = True)


def get_back_kb():

	builder = ReplyKeyboardBuilder()

	exit_btn = KeyboardButton(
		text = "↩️ Назад"
	)

	builder.add(exit_btn)

	return builder.as_markup(resize_keyboard = True)


def get_skip_kb():

	builder = ReplyKeyboardBuilder()

	skip_btn = KeyboardButton(
		text = "↪️ Пропустить"
	)

	exit_btn = KeyboardButton(
		text = "↩️ Назад"
	)

	builder.add(skip_btn, exit_btn)

	return builder.as_markup(resize_keyboard = True)


def get_mailer_finish_kb():

	builder = ReplyKeyboardBuilder()

	start_btn = KeyboardButton(
		text = "🟢 Начать рассылку"
	)

	exit_btn = KeyboardButton(
		text = "↩️ Назад"
	)

	builder.add(start_btn, exit_btn)

	return builder.as_markup(resize_keyboard = True, is_persistent = True)


def get_mailer_btn_ikb(buttons_preset: list[str]|None):

	if buttons_preset is None:
		return

	builder = InlineKeyboardBuilder()

	for btn_preset in buttons_preset:
		btn_data = [x.strip() for x in btn_preset.split("+")]
		btn_name = btn_data[0]
		btn_url = btn_data[1]

		builder.add(InlineKeyboardButton(
			text = btn_name,
			url = btn_url
		))

	builder.adjust(1)

	return builder.as_markup()
