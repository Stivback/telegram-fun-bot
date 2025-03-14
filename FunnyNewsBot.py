import asyncio
import aiohttp
import certifi
import ssl
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
import random

API_TOKEN = '7779371837:AAEOP4j9uclaHk9uiJPxQLviGyUkqzw6Tqg'  # Ваш токен
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
FACT_API_URL = "https://uselessfacts.jsph.pl/api/v2/facts/random"

# Запасной список фактов
FALLBACK_FACTS = [
    "Крокодилы могут жить до 100 лет, но не умеют смеяться.",
    "В Японии есть остров, где живут только кролики.",
    "Осьминоги могут менять цвет, чтобы сливаться с окружением.",
    "Самая короткая война в истории длилась 38 минут."
]

async def fetch_random_fact():
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(FACT_API_URL, ssl=ssl_context) as response:
                if response.status == 200:
                    data = await response.json()
                    return data["text"]
                else:
                    return random.choice(FALLBACK_FACTS)
    except Exception as e:
        print(f"Ошибка при запросе к API: {e}")
        return random.choice(FALLBACK_FACTS)

@dp.message(Command("start"))
async def send_welcome(message: Message):
    print(f"Получена команда /start от {message.from_user.id} в чате {message.chat.id}")
    await message.reply("Привет! Я бот с забавными фактами. Напиши /fact, чтобы получить факт!")

@dp.message(Command("fact"))
async def send_fact(message: Message):
    print(f"Получена команда /fact от {message.from_user.id} в чате {message.chat.id}")
    fact = await fetch_random_fact()
    await message.reply(fact)

@dp.message(Command("getid"))
async def get_chat_id(message: Message):
    print(f"Получена команда /getid от {message.from_user.id} в чате {message.chat.id}")
    await message.reply(f"ID этого чата: {message.chat.id}")

async def send_fact_to_chat():
    chat_id = -1001444039565  # Замените на ваш актуальный chat_id после проверки с /getid
    while True:
        try:
            fact = await fetch_random_fact()
            await bot.send_message(chat_id, fact)
            print(f"Факт отправлен в чат {chat_id}: {fact}")
        except Exception as e:
            print(f"Ошибка при отправке: {e}")
        await asyncio.sleep(3600)  # Каждые 60 минут

async def main():
    print("Бот запущен, начинаем polling...")
    asyncio.create_task(send_fact_to_chat())
    try:
        await dp.start_polling(bot)
    except Exception as e:
        print(f"Ошибка в polling: {e}")

if __name__ == '__main__':
    print("Запускаем бота...")
    asyncio.run(main())

