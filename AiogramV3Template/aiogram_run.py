# Bot
from create_bot import bot, dp, start_command

# Entry
from handlers.start import start_router
from handlers.admin.main import admin_main_router

# Client handlers

# Admin handlers
from handlers.admin.list_of_users import list_of_users_router
from handlers.admin.statistic import admin_statistic_router
from handlers.admin.management import admin_management_router
from handlers.admin.mailer import admin_mailer_router

# ORM
from database.orm import ORM as orm

# Another
from uvloop import run


async def main():

	await orm.proceed_schemas()
	await bot.set_my_commands(start_command)
	await orm.create_admin_if_not_exists(872114089, "@RubyHunter", "ruby")

	# ENTRY POINTS
	dp.include_router(start_router)
	dp.include_router(admin_main_router)

	# ADMIN
	dp.include_router(list_of_users_router)
	dp.include_router(admin_statistic_router)
	dp.include_router(admin_management_router)
	dp.include_router(admin_mailer_router)

	#await bot.delete_webhook(drop_pending_updates = True)
	await dp.start_polling(bot)


if __name__ == "__main__":
	run(main())
