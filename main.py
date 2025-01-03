import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from config import TOKEN

import random

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command('photo'))
async def photo(message: Message):
    list = ['https://img.freepik.com/free-vector/happy-mouse-holding-gold_1308-130334.jpg?auto=format&fit=crop&w=315&h=220',
        'https://img.freepik.com/free-vector/flat-cute-frog-illustration_52683-62357.jpg?auto=format&fit=crop&w=315&h=220',
        'https://img.freepik.com/free-vector/diverse-dogs-characters-collection_1308-133892.jpg?auto=format&fit=crop&w=315&h=220']
    rand_photo = random.choice(list)
    await message.answer_photo(photo=rand_photo, caption='Это супер крутая картинка')


# Прописываем хендлер и варианты ответов:
@dp.message(F.photo)
async def react_photo(message: Message):
    list = ['Ого, какая фотка!', 'Непонятно, что это такое.', 'Не отправляй мне такое больше!']
    rand_answ = random.choice(list)
    await message.answer(rand_answ)


@dp.message(F.text == 'Что такое ИИ?')
async def aitext(message: Message):
    await message.answer('Искусственный интеллект — это свойство искусственных интеллектуальных систем выполнять творческие функции, которые традиционно считаются прерогативой человека; наука и технология создания интеллектуальных машин, особенно интеллектуальных компьютерных программ')


@dp.message(Command('help'))
async def help(message: Message):
    await message.answer("Этот бот умеет выполнять команды:\n /start \n /help \n /photo")


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет, я бот!")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
