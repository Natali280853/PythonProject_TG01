from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from config import TOKEN

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


# Задание 1: Простое меню с кнопками
@dp.message(CommandStart())
async def start(message: Message):
    main = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Привет")],
        [KeyboardButton(text="Пока")]
    ], resize_keyboard=True)
    await message.answer("Выберите действие:", reply_markup=main)


@dp.message(lambda message: message.text == "Привет")
async def say_hello(message: types.Message):
    await message.answer(f"Привет, {message.from_user.first_name}!")


@dp.message(lambda message: message.text == "Пока")
async def say_goodbye(message: types.Message):
    await message.answer(f"До свидания, {message.from_user.first_name}!")


# Задание 2: Кнопки с URL-ссылками
inline_keyboard_test = InlineKeyboardMarkup(inline_keyboard=[
   [InlineKeyboardButton(text="Новости", url="https://news.ycombinator.com/")],
   [InlineKeyboardButton(text="Музыка", url="https://www.spotify.com/")],
   [InlineKeyboardButton(text="Видео", url="https://www.youtube.com/")]
])


@dp.message(Command('links'))
async def cmd_links(message: Message):
    await message.answer(f'Выберите ссылку:', reply_markup=inline_keyboard_test)


# Задание 3: Динамическое изменение клавиатуры
@dp.message(Command('dynamic'))
async def cmd_dynamic(message: Message):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Показать больше", callback_data="show_more")]
    ])
    await message.answer("Нажмите на кнопку:", reply_markup=markup)

# @dp.callback_query(F.callback_data == "show_more")
# async def show_more(callback: CallbackQuery):
#     markup = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text="Опция 1", callback_data="option_1")],
#     [InlineKeyboardButton(text="Опция 2", callback_data="option_2")]
#     ])
#     await callback.message.edit_text('aa', reply_markup=markup)
#     await callback.answer()  # Убираем кружок загрузки

kb_option = ["Опция 1", "Опция 2"]

# async def opt_keyboard():
#     keyboard = ReplyKeyboardBuilder()
#     for key in kb_option:
#         keyboard.add(KeyboardButton(text=key))
#     return keyboard.adjust(1).as_markup()

async def opt_keyboard():
    keyboard = InlineKeyboardBuilder()
    for key in kb_option:
        keyboard.add(InlineKeyboardButton(text=key, callback_data=key.lower().replace(" ", "_")))  # Добавляем callback_data для кнопок
    return keyboard.adjust(1).as_markup()


@dp.callback_query(F.data == 'show_more')
async def show_more(callback: CallbackQuery):
    await callback.message.edit_text('Нажмите на кнопку:', reply_markup=await opt_keyboard())


@dp.callback_query(F.data == "опция_1")  # Обратите внимание на изменение здесь
async def option_1(callback: CallbackQuery):
    await callback.message.answer("Вы выбрали Опцию 1!")
    await callback.answer()  # Убираем кружок загрузки


@dp.callback_query(F.data == "опция_2")  # Обратите внимание на изменение здесь
async def option_2(callback: CallbackQuery):
    await callback.message.answer("Вы выбрали Опцию 2!")
    await callback.answer()  # Убираем кружок загрузки


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
