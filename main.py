import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from config import TOKEN
from gtts import gTTS
import os
import random

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command('photo'))  # , prefix='&'))
async def photo(message: Message):
    list = ['https://cdn.stocksnap.io/img-thumbs/280h/coffee-beans_SRE9CWE7SW.jpg',
        'https://cdn.stocksnap.io/img-thumbs/280h/birthday-party_SRV2U52721.jpg',
        'https://cdn.stocksnap.io/img-thumbs/280h/IIVH2LDF2X.jpg']
    rand_photo = random.choice(list)
    await message.answer_photo(photo=rand_photo, caption='Это супер крутая картинка')

# Прописываем хендлер и варианты ответов:
@dp.message(F.photo)
async def react_photo(message: Message):
    list = ['Ого, какая фотка!', 'Непонятно, что это такое.', 'Не отправляй мне такое больше!']
    rand_answ = random.choice(list)
    await message.answer(rand_answ)
# Почему мы используем -1 в квадратных скобках? Когда мы отправляем фотографию, Telegram отправляет несколько
# ее копий в разных размерах. Мы выбираем последнюю версию, так как она имеет максимальный доступный размер и
# наиболее удобна для нас. Поэтому указываем -1, что означает последнюю версию изображения. И, наконец, мы
# указываем ID фотографии, чтобы присвоить ей уникальное имя.
    await bot.download(message.photo[-1], destination=f'tmp/{message.photo[-1].file_id}.jpg')


@dp.message(Command('video'))
async def video(message: Message):
    await bot.send_chat_action(message.chat.id, 'upload_video')
    video = FSInputFile('Даша_Лиза.MOV')
    await bot.send_video(message.chat.id, video)


@dp.message(Command('audio'))
async def audio(message: Message):
    audio = FSInputFile('Валенки.mp3')
    await bot.send_audio(message.chat.id, audio)


@dp.message(Command('voice'))
async def voice(message: Message):
    voice = FSInputFile("sample.ogg")
    #      await bot.send_voice(message.chat.id, voice)
    await message.answer_voice(voice)


@dp.message(Command('training'))
async def training(message: Message):
    training_list = [
        "Тренировка 1:\n1. Скручивания: 3 подхода по 15 повторений\n2. Велосипед: 3 подхода по 20 повторений (каждая сторона)\n3. Планка: 3 подхода по 30 секунд",
        "Тренировка 2:\n1. Подъемы ног: 3 подхода по 15 повторений\n2. Русский твист: 3 подхода по 20 повторений (каждая сторона)\n3. Планка с поднятой ногой: 3 подхода по 20 секунд (каждая нога)",
        "Тренировка 3:\n1. Скручивания с поднятыми ногами: 3 подхода по 15 повторений\n2. Горизонтальные ножницы: 3 подхода по 20 повторений\n3. Боковая планка: 3 подхода по 20 секунд (каждая сторона)"
    ]
    rand_tr = random.choice(training_list)
    await message.answer(f"Это ваша мини-тренировка на сегодня\n {rand_tr}")
   # tts = gTTS(text=rand_tr, lang='ru')   # озвучка текста rand_tr в формате mp3
   # tts.save("training.mp3")
   # audio = FSInputFile('training.mp3')
   # await bot.send_audio(message.chat.id, audio)
   # os.remove("training.mp3")
    tts = gTTS(text=rand_tr, lang='ru')  # озвучка текста rand_tr в формате ogg (голосовое сообщение)
    tts.save("training.ogg")
    audio = FSInputFile("training.ogg")
    await bot.send_voice(message.chat.id, voice=audio)
    os.remove("training.ogg")


@dp.message(Command('doc'))
async def doc(message: Message):
    doc = FSInputFile("sql_primer.pdf")
    await bot.send_document(message.chat.id, doc)


@dp.message(F.text == 'Что такое ИИ?')
async def aitext(message: Message):
    await message.answer('Искусственный интеллект — это свойство искусственных интеллектуальных систем выполнять творческие функции, которые традиционно считаются прерогативой человека; наука и технология создания интеллектуальных машин, особенно интеллектуальных компьютерных программ')


@dp.message(Command('help'))
async def help(message: Message):
    await message.answer("Этот бот умеет выполнять команды:\n /start \n /help \n /photo")


@dp.message(CommandStart())  # = /start
async def start(message: Message):
    await message.answer(f"Привет, {message.from_user.first_name}!")  # full_name


# общий случай на необъявленную команду = else. ПРописывается последним.
@dp.message()
async def start(message: Message):
    if message.text.lower() == 'тест':
        await message.answer("тестируем")
      #  await message.send_copy(chat_id=message.chat.id)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
