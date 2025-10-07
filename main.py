import asyncio
import logging
from aiogram import Bot, Dispatcher
from handler.router import router

# Твой токен бота
BOT_TOKEN = "8469918338:AAHvoFEjjzB0R7S8fQ0t5LDDerUsfx8m1to"

# Настройка логов
logging.basicConfig(level=logging.INFO)

# Основная функция запуска
async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Подключаем маршрутизатор
    dp.include_router(router)

    logging.info("✅ Bot started. Press Ctrl+C to stop.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("❌ Bot stopped.")
