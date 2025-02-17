# Aiogram
import aiogram.types as types
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest

# Const
from create_bot import orm

# Keyboards
from keyboards.admin.main_kbs import *

# States
from states.admin_states import AdminStates, AdminBlacklistStates

# Another
from contextlib import suppress


# Init
admin_blacklist_router = Router()


@admin_blacklist_router.message(F.text == "🚫 Черный список", StateFilter(AdminStates.main))
@admin_blacklist_router.message(F.text == "↩️ Назад", StateFilter(AdminBlacklistStates))
async def cmd_blacklist(message: types.Message, state: FSMContext):

	msg_text = "🚫 Выберите действие:"

	await message.answer(
		text = msg_text,
		reply_markup = get_blacklist_kb()
	)

	await state.set_state(AdminBlacklistStates.main)


#*############################
#*#           ADD            #
#*############################


@admin_blacklist_router.message(F.text == "➕ Добавить", StateFilter(AdminBlacklistStates.main))
async def cmd_blacklist_add(message: types.Message, state: FSMContext):

	msg_text = f"➕ Введите User ID:"

	await message.answer(
		text = msg_text,
		reply_markup = get_back_kb()
	)

	await state.set_state(AdminBlacklistStates.add_blacklist)


@admin_blacklist_router.message(F.text, StateFilter(AdminBlacklistStates.add_blacklist))
async def cmd_blacklist_add_finish(message: types.Message, state: FSMContext):

    # validation
	if not message.text.isdigit():
		await message.answer(
			text = "⛔️ Только цифры! Повторите попытку:",
			reply_markup = get_back_kb()
		)
		return

	user_id = int(message.text)

	if not await orm.is_user_exists(user_id):
		await message.answer(
			text = "⛔️ Пользователь не существует в БД! Повторите попытку:",
			reply_markup = get_back_kb()
		)
		return

	await orm.create_blacklist(user_id = user_id)

	await message.answer(text = f"✅ Черный список обновлен!")
	await cmd_blacklist(message, state)


#*############################
#*#           DEL            #
#*############################


@admin_blacklist_router.message(F.text == "➖ Удалить", StateFilter(AdminBlacklistStates.main))
async def cmd_blacklist_delete(message: types.Message, state: FSMContext):

	msg_text = "➖ Введите User ID:"
	
	await message.answer(
		text = msg_text,
		reply_markup = get_back_kb()
	)

	await state.set_state(AdminBlacklistStates.del_blacklist)


@admin_blacklist_router.message(F.text, StateFilter(AdminBlacklistStates.del_blacklist))
async def cmd_blacklist_delete_finish(message: types.Message, state: FSMContext):

	 # validation
	if not message.text.isdigit():
		await message.answer(
			text = "⛔️ Только цифры! Повторите попытку:",
			reply_markup = get_back_kb()
		)
		return

	user_id = int(message.text)

	if not await orm.is_blacklisted(user_id):
		await message.answer(
			text = "⛔️ Пользователь не найден в ЧС! Повторите попытку:",
			reply_markup = get_back_kb()
		)
		return

	await orm.delete_blacklist(user_id = user_id)

	await message.answer(
		text = f"✅ Черный список обновлен!"
	)

	await cmd_blacklist(message, state)


#*############################
#*#           LIST           #
#*############################


@admin_blacklist_router.message(F.text == "👁 Открыть список", StateFilter(AdminBlacklistStates.main))
async def cmd_blacklist_list(message: types.Message, state: FSMContext):

	await state.update_data(blacklist_offset = 0)
	items = await orm.get_all_blacklist()

	if not items:
		await message.answer(
			text = "💭 Список пуст."
		)
		return

	offset = 0
	max_offset = len(items) // 10 + (1 if len(items) % 10 != 0 else 0)

	msg_text = f"<b>🚫 Черный список {offset + 1}/{max_offset}</b>\n\n"

	for item in items[offset * 10:(offset + 1) * 10]:
		msg_text += f"✦ <code>{item}</code>\n"

	await message.answer(
		text = msg_text,
		reply_markup = get_bookList_ikb(
			prefix = "admin_blacklist",
			offset = 0,
			max_offset = max_offset,
			items = [],
			element_col = 10
		)
	)


async def cmd_blacklist_list_query(query: types.CallbackQuery, state: FSMContext):

	data = await state.get_data()
	offset = data.get("blacklist_offset")
	items = await orm.get_all_blacklist()
	
	if not items:
		await query.answer(
			text = "💭 Список пуст."
		)
		return
	
	max_offset = len(items) // 10 + (1 if len(items) % 10 != 0 else 0)

	if offset < 0:
		offset = max_offset - 1
		await state.update_data(blacklist_offset = offset)
	elif offset >= max_offset:
		offset = 0
		await state.update_data(blacklist_offset = offset)

	msg_text = f"<b>🚫 Черный список {offset + 1}/{max_offset}</b>\n\n"

	for item in items[offset * 10:(offset + 1) * 10]:
		msg_text += f"✦ <code>{item}</code>\n"

	with suppress(TelegramBadRequest):
		await query.message.edit_text(
			text = msg_text,
			reply_markup = get_bookList_ikb(
				prefix = "admin_blacklist",
				offset = offset,
				max_offset = max_offset,
				items = [],
				element_col = 10
			)
		)

	await query.answer()


@admin_blacklist_router.callback_query(F.data == "admin_blacklist_next", StateFilter(AdminBlacklistStates.main))
@admin_blacklist_router.callback_query(F.data == "admin_blacklist_prev", StateFilter(AdminBlacklistStates.main))
@admin_blacklist_router.callback_query(F.data == "admin_blacklist_status", StateFilter(AdminBlacklistStates.main))
async def cmd_blacklist_list_actions(query: types.CallbackQuery, state: FSMContext):

	state_data = await state.get_data()

	if query.data.endswith("next"):
		await state.update_data(blacklist_offset = state_data.get("blacklist_offset", 0) + 1)
	elif query.data.endswith("prev"):
		await state.update_data(blacklist_offset = state_data.get("blacklist_offset", 0) - 1)

	await cmd_blacklist_list_query(query, state)
