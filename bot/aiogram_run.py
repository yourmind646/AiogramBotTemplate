# Aiogram
from aiogram.types.bot_command_scope_all_private_chats import BotCommandScopeAllPrivateChats

# Bot
from create_bot import bot, dp, start_command, orm

# Entry
from handlers.start import start_router, types
from handlers.admin.main import admin_main_router

# Client handlers

# Admin handlers
from handlers.admin.list_of_users import list_of_users_router
from handlers.admin.statistic import admin_statistic_router
from handlers.admin.management import admin_management_router
from handlers.admin.mailer import admin_mailer_router
from handlers.admin.settings import admin_settings_router
from handlers.admin.blacklist import admin_blacklist_router

# middlewares
from middlewares.users_control import *
from middlewares.album import AlbumMiddleware

# Another
from decouple import config
from uvloop import run


async def main():

	await orm.proceed_schemas()
	await bot.set_my_commands(start_command, scope = BotCommandScopeAllPrivateChats())
	await orm.create_admin(int(config("BASE_ADMIN")), "base_admin", "base_admin")

	dp.message.middleware(BlacklistMiddleware())
	dp.callback_query.middleware(BlacklistMiddleware())
	dp.message.middleware(AntiFloodMiddleware())
	dp.message.middleware(AlbumMiddleware())

	# ENTRY POINTS
	dp.include_routers(
		start_router,
		admin_main_router
	)

	# CLIENT
	#dp.include_routers()

	# ADMIN
	dp.include_routers(
		list_of_users_router,
		admin_statistic_router,
		admin_management_router,
		admin_mailer_router,
		admin_settings_router,
		admin_blacklist_router
	)

	#await bot.delete_webhook(drop_pending_updates = True)
	await dp.start_polling(bot)


if __name__ == "__main__":
	run(main())
