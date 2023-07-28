# sqlalchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, BIGINT, VARCHAR, Boolean, DateTime, SmallInteger, ARRAY, DOUBLE_PRECISION


# init baseModel
BaseModel = declarative_base()


class User(BaseModel):

	__tablename__ = "users"

	user_id = Column(BIGINT, unique = True, primary_key = True, nullable = False)
	username = Column(VARCHAR(33), nullable = False)
	fullname = Column(VARCHAR(128), nullable = False)

