from aiogram import types
from aiogram import BaseMiddleware
from datetime import datetime, timedelta, timezone
from collections import deque
import asyncio

# Const
from create_bot import orm


class AntiFloodMiddleware(BaseMiddleware):
	
	def __init__(self, max_messages: int = 5, interval: float = 2, block_time: float = 60.0):
		"""
		Инициализация AntiFloodMiddleware.

		:param max_messages: Максимальное количество сообщений.
		:param interval: Временной интервал (в секундах) для проверки сообщений.
		:param block_time: Время блокировки пользователя (в секундах).
		"""
		super(AntiFloodMiddleware, self).__init__()
		self.max_messages = max_messages
		self.interval = interval
		self.block_time = block_time
		self.user_messages = {}  # user_id: deque of message timestamps
		self.blocked_users = {}  # user_id: unblock_time
		self.lock = asyncio.Lock()  # Для обеспечения потокобезопасности
	
	async def __call__(self, handler, event: types.Message, data):
		user_id = event.from_user.id
		current_time = datetime.now(timezone.utc)

		async with self.lock:
			# Проверка, заблокирован ли пользователь
			if user_id in self.blocked_users:
				unblock_time = self.blocked_users[user_id]
				if current_time < unblock_time:
					# Пользователь всё ещё заблокирован
					return
				else:
					# Блокировка истекла
					del self.blocked_users[user_id]

			if isinstance(event, types.CallbackQuery):
				return await handler(event, data)

			# Инициализация очереди сообщений для пользователя, если её ещё нет
			if user_id not in self.user_messages:
				self.user_messages[user_id] = deque()

			user_queue = self.user_messages[user_id]
			user_queue.append(current_time)

			# Удаление сообщений, которые старше интервала
			while user_queue and (current_time - user_queue[0]).total_seconds() > self.interval:
				user_queue.popleft()

			# Проверка, превысил ли пользователь лимит сообщений
			if len(user_queue) > self.max_messages:
				# Блокировка пользователя
				self.blocked_users[user_id] = current_time + timedelta(seconds = self.block_time)
				# Очистка очереди сообщений
				del self.user_messages[user_id]

				await event.answer(
					text = "🧊 Вы заморожены на 1 минуту за флуд!"
				)

				# Отмена обработки сообщения и блокировка
				return

		return await handler(event, data)


class BlacklistMiddleware(BaseMiddleware):
	def __init__(self):
		super().__init__()

	async def __call__(self, handler, event: types.Update, data: dict):
		user_id = self.get_user_id(event)
		if user_id:
			if await orm.is_blacklisted(user_id):
				return

		return await handler(event, data)
	
	def get_user_id(self, event: types.Update):
		return event.from_user.id
