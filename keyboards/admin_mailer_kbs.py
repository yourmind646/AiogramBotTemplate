# Aiogram imports
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_mailer_menu_kb():

	reply_markup = ReplyKeyboardMarkup(
		resize_keyboard = True,
		is_persistent = True
	)

	text_btn = KeyboardButton(
		text = "📝 Текст" 
	)

	image_btn = KeyboardButton(
		text = "🖼 Фото"
	)

	back_btn = KeyboardButton(
		text = "🔙 Вернуться в меню"
	)

	reply_markup.row(text_btn, image_btn)
	reply_markup.add(back_btn)

	return reply_markup


def get_back_kb():

	reply_markup = ReplyKeyboardMarkup(
		resize_keyboard = True
	)

	exit_btn = KeyboardButton(
		text = "🔙 Назад"
	)

	reply_markup.add(exit_btn)

	return reply_markup


def get_skip_kb():

	reply_markup = ReplyKeyboardMarkup(
		resize_keyboard = True
	)

	skip_btn = KeyboardButton(
		text = "↪️ Пропустить"
	)

	exit_btn = KeyboardButton(
		text = "🔙 Назад"
	)

	reply_markup.add(skip_btn, exit_btn)

	return reply_markup


def get_mailer_finish_kb():

	reply_markup = ReplyKeyboardMarkup(
		resize_keyboard = True,
		is_persistent = True
	)

	start_btn = KeyboardButton(
		text = "🟢 Начать рассылку"
	)

	exit_btn = KeyboardButton(
		text = "🔙 Назад"
	)

	reply_markup.add(start_btn, exit_btn)

	return reply_markup


def get_mailer_btn_ikb(buttons_preset: str):
	
	if buttons_preset is None:
		return

	inline_markup = InlineKeyboardMarkup(row_width = 1)

	for btn_preset in buttons_preset.split("\n"):
		btn_data = [x.strip() for x in btn_preset.split("+")]
		btn_name = btn_data[0]
		btn_url = btn_data[1]

		inline_markup.add(InlineKeyboardButton(
			text = btn_name,
			url = btn_url
		))

	return inline_markup
