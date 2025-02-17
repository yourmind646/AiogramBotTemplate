# Aiogram imports
import aiogram.types as types
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram import Router, F

# Const
from create_bot import orm

# Keyboards
from keyboards.admin.main_kbs import *

# States
from states.admin_states import AdminStates, AdminSettingsStates


# Init
admin_settings_router = Router()


@admin_settings_router.message(F.text == "↩️ Назад", StateFilter(AdminSettingsStates))
@admin_settings_router.message(F.text == "⚙️ Настройки", StateFilter(AdminStates.main))
async def cmd_settings(message: types.Message, state: FSMContext):
	
	msg_text = "⚙️ Выберите, что хотите изменить:"

	await message.answer(
		text = msg_text,
		reply_markup = get_settings_kb()
	)

	await state.set_state(AdminSettingsStates.main)


#*############################
#*#        EDIT PHOTO        #
#*############################


@admin_settings_router.message(F.text.in_({
	"🖼 ..."
}), StateFilter(AdminSettingsStates.main))
async def cmd_edit_photo(message: types.Message, state: FSMContext):

	x = {
		"🖼 ...": "..."
	}
	
	setting_key = x.get(message.text)
	await state.update_data(setting_key = setting_key)
	photo = await orm.get_setting_value(setting_key)

	msg_text = f"""<b>Текущее значение:</b>
<blockquote>{photo}</blockquote>

⌨️ Отправьте фото для изменения:"""

	if photo:
		await message.answer_photo(
			photo = photo,
			caption = msg_text,
			reply_markup = get_back_kb()
		)
	else:
		await message.answer(
			text = msg_text,
			reply_markup = get_back_kb()
		)

	await state.set_state(AdminSettingsStates.edit_photo)


@admin_settings_router.message(F.photo, StateFilter(AdminSettingsStates.edit_photo))
async def cmd_edit_photo_setup(message: types.Message, state: FSMContext):

	photo = message.photo[-1].file_id

	state_data = await state.get_data()
	setting_key = state_data.get("setting_key")

	await orm.update_setting_value(setting_key, photo)

	msg_text = f"""<b>Текущее значение:</b>
<blockquote>{photo}</blockquote>

⌨️ Отправьте фото для изменения:"""

	if photo:
		await message.answer_photo(
			photo = photo,
			caption = msg_text,
			reply_markup = get_back_kb()
		)
	else:
		await message.answer(
			text = msg_text,
			reply_markup = get_back_kb()
		)

	await state.set_state(AdminSettingsStates.edit_photo)
