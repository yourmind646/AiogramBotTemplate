# sqlalchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, BIGINT, VARCHAR, Boolean, DateTime, SmallInteger, ARRAY, DOUBLE_PRECISION, Enum
from sqlalchemy.dialects.postgresql import JSONB

# types
from database.db_types import *


# init baseModel
BaseModel = declarative_base()


class User(BaseModel):

	__tablename__ = "users"

	user_id = Column(BIGINT, primary_key = True)
	username = Column(VARCHAR(33), nullable = True)
	fullname = Column(VARCHAR(128), nullable = False)
	register_date = Column(DateTime(timezone = True), nullable = False)


class Admin(BaseModel):

	__tablename__ = "admins"

	user_id = Column(BIGINT, primary_key = True)
	username = Column(VARCHAR(33), nullable = True)
	fullname = Column(VARCHAR(128), nullable = False)


class Blacklist(BaseModel):

	__tablename__ = "blacklist"

	user_id = Column(BIGINT, primary_key = True)


class Setting(BaseModel):

	__tablename__ = "settings"

	name = Column(String, primary_key = True)
	value = Column(JSONB, nullable = True)
