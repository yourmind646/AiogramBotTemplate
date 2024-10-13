# sqlalchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, BIGINT, VARCHAR, Boolean, DateTime, SmallInteger, ARRAY, DOUBLE_PRECISION
from sqlalchemy.dialects.postgresql import JSONB


# init baseModel
BaseModel = declarative_base()


class User(BaseModel):

	__tablename__ = "users"

	user_id = Column(BIGINT, primary_key = True)
	username = Column(VARCHAR(33), nullable = False)
	fullname = Column(VARCHAR(128), nullable = False)
	register_date = Column(DateTime(timezone = True), nullable = False)


class Admin(BaseModel):

	__tablename__ = "admins"

	admin_user_id = Column(BIGINT, primary_key = True)
	admin_username = Column(VARCHAR(33), nullable = False)
	admin_fullname = Column(VARCHAR(128), nullable = False)
