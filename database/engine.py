# sqlalchemy imports
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine
from sqlalchemy.orm import sessionmaker

# another
from typing import Union


def create_async_engine(url: Union[URL, str]) -> AsyncEngine:
	
	return _create_async_engine(url = url, pool_pre_ping = True, pool_recycle = 3600)


def get_session_maker(engine: AsyncEngine) -> AsyncSession:
	
	return sessionmaker(engine, class_ = AsyncSession, expire_on_commit = False)