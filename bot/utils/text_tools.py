import re


def to_html(obj):
	
	return str(obj).replace("<", "&lt;").replace(">", "&gt;")


def parse_links_to_inline_markup(message: str) -> list:
	"""
	Парсит сообщение с форматированными ссылками и возвращает список рядов кнопок.

	Формат входного сообщения:
	- [Текст кнопки + Ссылка] для одной кнопки.
	- [Кнопка1 + Ссылка1][Кнопка2 + Ссылка2] для нескольких кнопок в одном ряду.
	- Каждая строка представляет отдельный ряд кнопок.

	Пример:
	[Кнопка1 + https://example.com]
	[Кнопка2 + https://example.org][Кнопка3 + https://example.net]

	:param message: Строка с отформатированными ссылками.
	:return: Список рядов кнопок, где каждый ряд — это список кортежей (Текст, Ссылка).
	"""
	# Исправленное регулярное выражение для поиска [Текст + Ссылка]
	pattern = re.compile(r'\[([^\[\]+]+)\s*\+\s*(https?://[^\[\]]+)\]')

	# Инициализируем список рядов кнопок
	keyboard_rows = []

	# Разбиваем сообщение на строки
	lines = message.strip().split('\n')
	
	for line in lines:
		# Находим все совпадения в строке
		matches = pattern.findall(line)
		if matches:
			row = []
			for text, url in matches:
				button = (text.strip(), url.strip())
				row.append(button)
			keyboard_rows.append(row)

	return keyboard_rows
