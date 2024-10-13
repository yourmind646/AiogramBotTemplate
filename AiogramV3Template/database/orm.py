# sqlalchemy import
from sqlalchemy import update, select, delete

# Database engine
from database.engine import create_async_engine, get_session_maker

# DB Models
from database.db_models import *

# Config
from decouple import config

# Another
from datetime import datetime


# create engine
async_engine = create_async_engine(
        url = f"postgresql+asyncpg://{config('DB_USERNAME')}:{config('DB_PASSWORD')}@{config('DB_HOST')}:{config('DB_PORT')}/{config('DB_NAME')}"
)

# create session_maker
session_maker = get_session_maker(async_engine)


class ORM:

	@staticmethod
	async def proceed_schemas() -> None:
		async with async_engine.begin() as conn:
			await conn.run_sync(BaseModel.metadata.create_all)


	### USERS MANAGEMENT
	@staticmethod
	async def is_user_exists(user_id: int) -> bool:
		async with session_maker() as session:
			async with session.begin():
				query = await session.execute(select(User.user_id).where(User.user_id == user_id))

				return query.one_or_none() is not None


	@staticmethod
	async def create_user_if_not_exists(user_id: int, username: str, fullname: str, register_date: datetime) -> None:
		async with session_maker() as session:
			async with session.begin():
				if not await ORM.is_user_exists(user_id):
					user = User(
						user_id = user_id,
						username = username,
						fullname = fullname,
						register_date = register_date
					)
					
					await session.merge(user)

					return True
				else:
					return False


	@staticmethod
	async def set_users_field(user_id: int, field: str, value: int|str|bool) -> None:
		async with session_maker() as session:
			async with session.begin():
				await session.execute(update(User).where(User.user_id == user_id).values({getattr(User, field): value}))
	

	@staticmethod
	async def get_user(user_id: int) -> User:
		async with session_maker() as session:
			async with session.begin():
				query = await session.scalars(select(User).where(User.user_id == user_id))

				return query.one_or_none()


	@staticmethod
	async def get_all_users() -> list[User]:
		async with session_maker() as session:
			async with session.begin():
				query = await session.scalars(select(User))

				return query.all()


	### ADMINS
	@staticmethod
	async def is_admin_exists(admin_user_id: int) -> bool:
		async with session_maker() as session:
			async with session.begin():
				query = await session.execute(select(Admin.admin_user_id).where(Admin.admin_user_id == admin_user_id))

				return query.one_or_none() is not None


	@staticmethod
	async def create_admin_if_not_exists(admin_user_id: int, admin_username: str, admin_fullname: str) -> None:
		async with session_maker() as session:
			async with session.begin():
				if not await ORM.is_admin_exists(admin_user_id):
					admin = Admin(
						admin_user_id = admin_user_id,
						admin_username = admin_username,
						admin_fullname = admin_fullname
					)
					
					await session.merge(admin)


	@staticmethod
	async def get_admin(admin_user_id: int) -> Admin:
		async with session_maker() as session:
			async with session.begin():
				query = await session.scalars(select(Admin).where(Admin.admin_user_id == admin_user_id))

				return query.one_or_none()
			

	@staticmethod
	async def get_all_admins() -> list[Admin]:
		async with session_maker() as session:
			async with session.begin():
				query = await session.scalars(select(Admin))

				return query.all()
			

	@staticmethod
	async def del_admin(admin_user_id: int) -> None:
		async with session_maker() as session:
			async with session.begin():
				await session.execute(delete(Admin).where(Admin.admin_user_id == admin_user_id))

	
	@staticmethod
	async def set_admin_field(admin_user_id: int, field: str, value: int|str|bool) -> None:
		async with session_maker() as session:
			async with session.begin():
				await session.execute(update(Admin).where(Admin.admin_user_id == admin_user_id).values({getattr(Admin, field): value}))