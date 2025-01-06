from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

# Создаём вложенные списки для рядов клавиатуры
# Дополняем содержимое круглых скобок командой resize_keyboard=True.
main = ReplyKeyboardMarkup(keyboard=[
   [KeyboardButton(text="Тестовая кнопка 1")],
   [KeyboardButton(text="Тестовая кнопка 2"), KeyboardButton(text="Тестовая кнопка 3")]
], resize_keyboard=True)


# inline_keyboard_test = InlineKeyboardMarkup(inline_keyboard=[
#    [InlineKeyboardButton(text="Видео", url='https://rutube.ru/shorts/1dad135b3f2bac8fac09e8285ab956a2/')]
# ])
# ниже inline_keyboard_test переопределяется

# Допустим, нам нужно достать из базы данных список. который часто меняется. В таком случае, чтобы не
# создавать новые кнопки, не менять клавиатуры, можно использовать  билдер,  который будет автоматически
# создавать клавиатуру из элементов полученного списка.
test = ["кнопка 1", "кнопка 2", "кнопка 3", "кнопка 4"]


# async def test_keyboard():
#     keyboard = ReplyKeyboardBuilder()
#     for key in test:
#         keyboard.add(KeyboardButton(text=key))
#     return keyboard.adjust(2).as_markup()
async def test_keyboard():
   keyboard = InlineKeyboardBuilder()
   for key in test:
       keyboard.add(InlineKeyboardButton(text=key, url='https://rutube.ru/shorts/1dad135b3f2bac8fac09e8285ab956a2/'))
   return keyboard.adjust(2).as_markup()


inline_keyboard_test = InlineKeyboardMarkup(inline_keyboard=[
   [InlineKeyboardButton(text="Каталог", callback_data='catalog')],
   [InlineKeyboardButton(text="Новости", callback_data='news')],
   [InlineKeyboardButton(text="Профиль", callback_data='person')]
])
