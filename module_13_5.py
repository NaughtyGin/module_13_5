from aiogram import  Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
import asyncio


api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
# button_calc = KeyboardButton(text='Рассчитать')
# button_info = KeyboardButton(text='Информация')
# kb.add(button_calc)
# kb.add(button_info)
buttons = ['Информация', 'Рассчитать']
kb.add(*buttons)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

# Упрощенный вариант формулы Миффлина-Сан Жеора для мужчин
@dp.message_handler(commands=['start'])
async def all_massages(message):
    await message.answer('Привет! Я бот, помогающий Вашему здоровью!', reply_markup=kb)
    await message.answer('Нажмите кнопку "Рассчитать", чтобы узнать суточную норму Ваших калорий')

@dp.message_handler(text=['Рассчитать'])
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(text=['Информация'])
async def set_age(message):
    await message.answer('Использован упрощенный вариант формулы Миффлина-Сан Жеора для мужчин')

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост (см):')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес (кг):')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    await UserState.weight.set()
    data = await state.get_data()
    await message.answer(f"Ваша норма калорий: "
                         f"{10 * float(data['weight']) + 6.25 * float(data['growth']) - 5 * float(data['age']) + 5}")
    await state.finish()

@dp.message_handler()
async def all_massages(message):
    await message.answer('Введите команду /start, чтобы начать общение')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
