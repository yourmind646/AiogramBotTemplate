# sqlalchemy import
from sqlalchemy import update, select, delete
from sqlalchemy.ext.asyncio import AsyncSession

# Database engine
from database.engine import create_async_engine, get_session_maker

# DB Models
from database.db_models import *

# My modules
from modules.cfg_loader import load_config

# Another
from datetime import datetime


# Load cfg
db_config = load_config("cfg/db_config.json")

# create engine
async_engine = create_async_engine(
	url = f"postgresql+asyncpg://{db_config.get('user')}:{db_config.get('password')}@{db_config.get('host')}:5432/{db_config.get('database')}"
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

				if query.one_or_none() is None:
					return False
				else:
					return True


	@staticmethod
	async def create_user_if_not_exists(user_id: int, username: str, fullname: str) -> None:
		async with session_maker() as session:
			async with session.begin():
				if not await ORM.is_user_exists(user_id):
					user = User(
						user_id = user_id,
						username = username,
						fullname = fullname
					)
					
					await session.merge(user)

					return True
				else:
					return False


	@staticmethod
	async def set_field(user_id: int, field: str, value: int|str|bool) -> None:
		async with session_maker() as session:
			async with session.begin():
				await session.execute(update(User).where(User.user_id == user_id).values({getattr(User, field): value}))
	

	@staticmethod
	async def get_user(user_id: int) -> User:
		async with session_maker() as session:
			async with session.begin():
				query = await session.scalars(select(User).where(User.user_id == user_id))

				return query.one_or_none()
