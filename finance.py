import asyncio
import logging
import os

from dotenv import load_dotenv
from aiogram import Dispatcher, Bot
from handlers.user_handler import user_router

logger = logging.getLogger(__name__)

load_dotenv()

async def main():
	# Базовая конфигурация логгера
	logging.basicConfig(
		level=logging.INFO,
		format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
	)


	bot_token = os.environ['BOT_TOKEN']
	# Инициализация Бота
	bot = Bot(token=bot_token)

	# Создание Диспетчера - центра управления запросами телеги
	dp = Dispatcher()

	# Присоединение к диспетчеру роутеров (локальных управленцев запросами) из файлов
	dp.include_router(user_router)

	await dp.start_polling(bot)

if __name__ == '__main__':
	asyncio.run(main())
