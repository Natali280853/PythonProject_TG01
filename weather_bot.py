import logging
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from aiogram.utils import executor
from aiogram import executor
from config import TOKEN

API_KEY = '272009fd696656bbaea88b8d974dd950'  # Замените на ваш ключ API
# TELEGRAM_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'  # Замените на токен вашего бота
CITY = 'Tyumen'  # Укажите город

bot = Bot(token=TOKEN)
# storage = MemoryStorage()
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply('Привет! Я бот погоды. Напиши /weather, чтобы получить прогноз погоды.')


@dp.message_handler(commands=['weather'])
async def get_weather(message: types.Message):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        temp = data['main']['temp']
        weather_desc = data['weather'][0]['description']
        await message.reply(f'Температура в {CITY}: {temp}°C\nОписание: {weather_desc}')
    else:
        await message.reply('Не удалось получить данные о погоде.')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)