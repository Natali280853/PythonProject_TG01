import sqlite3
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile

# Эта библиотека нужна для сохранения контекста между сообщениями, чтобы сохранять информацию между запросами и использовать ее, например, в базе данных.
from aiogram.fsm.context import FSMContext

# импортируем библиотеку для работы с состояниями, или другими словами, для работы с информацией, передаваемой пользователем. Здесь будет использоваться класс State для работы с отдельными состояниями пользователей и StatesGroup для группировки состояний.
from aiogram.fsm.state import State, StatesGroup

# импортируем библиотеку для сохранения состояния в оперативной памяти:
from aiogram.fsm.storage.memory import MemoryStorage

# библиотека — IOHTTP для выполнения асинхронных HTTP-запросов. Наш бот будет подключаться к API прогнозов погоды и выдавать прогноз для конкретного пользователя, город которого будет записан в базе данных.
import aiohttp

# здесь можно также использовать логирование, что, по сути, является ведением журнала событий. Это полезно для записи сообщений, событий или информации о работе программы. Для этого импортируем библиотеку Logging:
import logging

from config import TOKEN, WEATHER_API_KEY


bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)


class Form(StatesGroup):
    # пропишем сведения, которые будем собирать у пользователя. эти состояния будут использоваться
    # для хранения и отслеживания, когда бот будет продолжать работу с пользователем.
    name = State()
    age = State()
    city = State()


#  создаем базу данных, в которую будет сохраняться информация от пользователя.
#  База данных не будет пересоздаваться при каждом запуске программы, так как мы прописали в коде
#  if not exists
def init_db():
    conn = sqlite3.connect('user_data.db')
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    city TEXT NOT NULL)
    ''')
    conn.commit()
    conn.close()


init_db()


@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer("Привет! Как тебя зовут?")
# С помощью await выполняем действие: state.set_state(Form.name).
# Это состояние указывает программе, что следующим шагом в диалоге будет ожидание ответа от пользователя.
# Мы отправили запрос на получение имени и программа ждет ответ
    await state.set_state(Form.name)


@dp.message(Form.name)  # =бот получил имя
async def name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Сколько тебе лет?")
    await state.set_state(Form.age)


# функцию для обработки возраста пользователя. Функция будет похожа на предыдущую, но здесь мы будем
# сохранять не имя, а возраст, а также запрашивать следующий вопрос: message.answer("Из какого ты города?").
@dp.message(Form.age)  # =бот получил возраст
async def age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("Из какого ты города?")
    await state.set_state(Form.city)


@dp.message(Form.city)
async def city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    user_data = await state.get_data()   # возвращает словарь с данными состояния

    conn = sqlite3.connect('user_data.db')
    cur = conn.cursor()
    cur.execute('''
    INSERT INTO users (name, age, city) VALUES (?, ?, ?)''', (user_data['name'], user_data['age'], user_data['city']))
    conn.commit()
    conn.close()

# создаем асинхронную сессию клиента
    async with aiohttp.ClientSession() as session:
    # создаёт асинхронную сессию и выполняет GET-запрос к API. результат запроса в переменной response
        async with session.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={user_data['city']}&appid={WEATHER_API_KEY}&units=metric") as response:
            if response.status == 200:
                weather_data = await response.json()
                main = weather_data['main']
                weather = weather_data['weather'][0]

                temperature = main['temp']
                humidity = main['humidity']  # влажность
                description = weather['description']  # описание погоды

                weather_report = (f"Город - {user_data['city']}\n"
                                  f"Температура - {temperature}\n"
                                  f"Влажность воздуха - {humidity}\n"
                                  f"Описание погоды - {description}")
                await message.answer(weather_report)
            else:
                await message.answer("Не удалось получить данные о погоде")
        await state.clear()


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
