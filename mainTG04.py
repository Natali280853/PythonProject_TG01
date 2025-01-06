import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile, CallbackQuery

from config import TOKEN
import keyboards as kb

bot = Bot(token=TOKEN)
dp = Dispatcher()


# При отправке команды мы будем получать сообщение, а внизу отобразится клавиатура.
# Используем “reply_markup” — аргумент функции, который позволит что-то дополнительно отображать.
@dp.message(CommandStart())
async def start(message: Message):
    # await message.answer(f'Привет, {message.from_user.first_name}', reply_markup=kb.inline_keyboard_test)
    # await message.answer(f'Привет, {message.from_user.first_name}', reply_markup= await kb.test_keyboard())
    #  await message.answer(f'Привет, {message.from_user.first_name}', reply_markup=kb.main)
    await message.answer(f'Привет, {message.from_user.first_name}', reply_markup=kb.inline_keyboard_test)


# Callback — это запрос. Его нужно обрабатывать. Для этого в файле main.py создаём обработчик.
# В обработчике создаём асинхронную функцию.
@dp.callback_query(F.data == 'news')
async def news(callback: CallbackQuery):
    await callback.answer("Новости подгружаются", show_alert=True)  # всплывае alert/ Если в "", то просто убирается значок ожидания на кнопке
    await callback.message.edit_text('Вот свежие новости!', reply_markup=await kb.test_keyboard())


@dp.message(F.text == "Тестовая кнопка 1")
async def test_button(message: Message):
   await message.answer('Обработка нажатия на reply кнопку')


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
