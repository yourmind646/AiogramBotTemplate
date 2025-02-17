# sqlalchemy import
from sqlalchemy import update, select, delete, func

# Database engine
from database.engine import create_async_engine, get_session_maker

# DB Models
from database.db_models import *

# Config
from decouple import config

# Another
from datetime import datetime
from typing import Any


class ORM:

	def __init__(self):
		self.async_engine = create_async_engine(
			url = f"postgresql+asyncpg://{config('POSTGRES_USER')}:{config('POSTGRES_PASSWORD')}@{config('POSTGRES_HOST')}:{config('POSTGRES_PORT')}/{config('POSTGRES_DB')}"
		)
		self.session_maker = get_session_maker(self.async_engine)


	async def proceed_schemas(self) -> None:
		async with self.async_engine.begin() as conn:
			await conn.run_sync(BaseModel.metadata.create_all)


	#*############################
	#*#          USERS           #
	#*############################


	async def is_user_exists(self, user_id: int) -> bool:
		async with self.session_maker() as session:
			async with session.begin():
				query = await session.execute(select(User.user_id).where(User.user_id == user_id))

				return query.one_or_none() is not None


	async def create_user(self, user_id: int, username: str, fullname: str, register_date: datetime) -> int:
		async with self.session_maker() as session:
			async with session.begin():
				if not await self.is_user_exists(user_id):
					user = User(
						user_id = user_id,
						username = username,
						fullname = fullname,
						register_date = register_date
					)
					
					session.add(user)
					await session.flush()
					return user.user_id
				else:
					return


	async def set_users_field(self, user_id: int, field: str, value: int|str|bool) -> None:
		async with self.session_maker() as session:
			async with session.begin():
				await session.execute(update(User).where(User.user_id == user_id).values({getattr(User, field): value}))
	

	async def get_user(self, user_id: int) -> User:
		async with self.session_maker() as session:
			async with session.begin():
				query = await session.scalars(select(User).where(User.user_id == user_id))

				return query.one_or_none()


	async def get_all_users(self) -> list[User]:
		async with self.session_maker() as session:
			async with session.begin():
				query = await session.scalars(select(User))

				return query.all()
			
	
	async def get_users_count(self) -> int:
		async with self.session_maker() as session:
			async with session.begin():
				query = await session.scalars(select(func.count()).select_from(User))

				return query.one_or_none()


	async def get_all_user_ids(self) -> list[int]:
		async with self.session_maker() as session:
			async with session.begin():
				query = await session.scalars(select(User.user_id))

				return query.all()


	#*############################
	#*#          ADMINS          #
	#*############################


	async def is_admin_exists(self, user_id: int) -> bool:
		async with self.session_maker() as session:
			async with session.begin():
				query = await session.execute(select(Admin.user_id).where(Admin.user_id == user_id))

				return query.one_or_none() is not None


	async def create_admin(self, user_id: int, username: str, fullname: str) -> None:
		async with self.session_maker() as session:
			async with session.begin():
				admin = Admin(
					user_id = user_id,
					username = username,
					fullname = fullname
				)
				
				await session.merge(admin)


	async def get_admin(self, user_id: int) -> Admin:
		async with self.session_maker() as session:
			async with session.begin():
				query = await session.scalars(select(Admin).where(Admin.user_id == user_id))

				return query.one_or_none()


	async def get_all_admins(self) -> list[Admin]:
		async with self.session_maker() as session:
			async with session.begin():
				query = await session.scalars(select(Admin))

				return query.all()


	async def delete_admin(self, user_id: int) -> None:
		async with self.session_maker() as session:
			async with session.begin():
				await session.execute(delete(Admin).where(Admin.user_id == user_id))


	async def set_admin_field(self, user_id: int, field: str, value: int|str|bool) -> None:
		async with self.session_maker() as session:
			async with session.begin():
				await session.execute(update(Admin).where(Admin.user_id == user_id).values({getattr(Admin, field): value}))


	#*############################
	#*#         SETTINGS         #
	#*############################


	async def is_setting_exists(self, name: str) -> bool:
		async with self.session_maker() as session:
			async with session.begin():
				query = await session.execute(select(Setting).where(Setting.name == name))

				return query.one_or_none() is not None


	async def create_setting(self, name: str, value: Any) -> None:
		async with self.session_maker() as session:
			async with session.begin():
				setting = Setting(
					name = name,
					value = value
				)
				
				await session.merge(setting)


	async def init_settings(self) -> None:

		...


	async def get_setting_value(self, name: str) -> Any:
		async with self.session_maker() as session:
			async with session.begin():
				query = await session.scalars(select(Setting.value).where(Setting.name == name))

				return query.one_or_none()


	async def update_setting_value(self, name: str, value: dict|list) -> None:
		async with self.session_maker() as session:
			async with session.begin():
				await session.execute(update(Setting).where(Setting.name == name).values({getattr(Setting, "value"): value}))


	#*############################
	#*#        BLACKLIST         #
	#*############################


	async def is_blacklisted(self, user_id: int) -> bool:
		async with self.session_maker() as session:
			async with session.begin():
				query = await session.execute(select(Blacklist).where(Blacklist.user_id == user_id))

				return query.one_or_none() is not None


	async def create_blacklist(self, user_id: int) -> None:
		async with self.session_maker() as session:
			async with session.begin():
				blacklist = Blacklist(
					user_id = user_id
				)
				
				await session.merge(blacklist)


	async def get_all_blacklist(self) -> list[int]:
		async with self.session_maker() as session:
			async with session.begin():
				query = await session.scalars(select(Blacklist.user_id).order_by(Blacklist.user_id))

				return query.all()


	async def delete_blacklist(self, user_id: int) -> None:
		async with self.session_maker() as session:
			async with session.begin():
				await session.execute(delete(Blacklist).where(Blacklist.user_id == user_id))
