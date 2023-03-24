# PostgreSQL import
import psycopg2

# Connect to pg server
try:
	connection = psycopg2.connect(
		host = 'localhost',
		user = 'postgres',
		password = 'diman030405',
		database = 'birzha'
	)
	connection.autocommit = True
except Exception as _ex:
	print(f'[INFO] Error while connecting to pdb - {_ex}')


class PSQLManager:

	# Is user exists checking
	@staticmethod
	async def is_user_exists(user_id):
		with connection.cursor() as cursor:
			cursor.execute(f"""SELECT user_id FROM users WHERE user_id = {user_id};""")
			
			result = cursor.fetchone()

			if result is None:
				return False
			else:
				return True


	# If the user does not exist, then create him
	@staticmethod
	async def create_user_if_not_exists(user_id, user_username):
		if not await PSQLManager.is_user_exists(user_id):
			with connection.cursor() as cursor:
				# Initialize data tuple
				data = (
					user_id, 0, 0, 0, 0, 0, # user data
					"0", "0", "0", "0", 0, "0", "0", "0", "0", "0", # post data
					user_username
				)
				# Executing
				cursor.execute(f"""INSERT INTO users VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""", data)

				return True
		else:
			return False


	# Add click
	@staticmethod
	async def set_field(user_id: int, field: str, value):
		with connection.cursor() as cursor:
			try:
				if isinstance(value, str):
					cursor.execute(f"""UPDATE users SET {field} = '{value}' WHERE user_id = {user_id};""")
				else:
					cursor.execute(f"""UPDATE users SET {field} = {value} WHERE user_id = {user_id};""")

				return True
			except Exception as e:
				print(e)


	@staticmethod
	async def get_field(user_id: int, field: str):
		with connection.cursor() as cursor:
			cursor.execute(f"""SELECT {field} FROM users WHERE user_id = {user_id}""")

			result = cursor.fetchone()[0]

			return result