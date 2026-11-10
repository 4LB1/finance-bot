import asyncio
from aiogram import Dispatcher, types, Bot, F
from aiogram.filters import Command

dp = Dispatcher()

inline_kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Income", callback_data="Income"), types.InlineKeyboardButton(text="Expense", callback_data="Expense")], 
        [types.InlineKeyboardButton(text="Show All Incomes", callback_data="Show_All_Incomes"), types.InlineKeyboardButton(text="Show All Expenses", callback_data="Show All Expenses")]
        ])

@dp.callback_query(F.data == 'menu')
@dp.message(Command('start'))
async def start(thing):
    if isinstance(thing, types.Message): await thing.answer("Добро пожаловать в финансовый помощник молодёжного служения A-life.\nВыберите, что вы хотели бы сделать:", reply_markup=inline_kb)
    if isinstance(thing, types.CallbackQuery) and isinstance(thing.message, types.Message): await thing.message.edit_text("Добро пожаловать в финансовый помощник молодёжного служения A-life.\nВыберите, что вы хотели бы сделать:", reply_markup=inline_kb)

@dp.callback_query(F.data == 'Income')
async def income_handler(query: types.CallbackQuery):
    await query.answer(text="Обработано")

@dp.callback_query(F.data == 'Show_All_Incomes')
async def show_income_handler(query: types.CallbackQuery):
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text='Go back?', callback_data='menu')]
    ])
    if isinstance(query.message, types.Message): await query.message.edit_text('Обработано', reply_markup=kb)

@dp.callback_query(F.data == 'Expense')
async def expense_handler(query: types.CallbackQuery):
    await query.answer(text="Обработано", show_alert=True)

@dp.callback_query(F.data == 'Show All Expenses')
async def show_expense_handler(query: types.CallbackQuery):
    await query.answer(text="Обработано")

@dp.message()
async def data_getting(message: types.Message):
    await message.answer("Данные добавлены.")

async def main() :

    bot = Bot("8310615846:AAEaKg57TT8IVmRm9DD00bxTWO3CV4PSQd4")
    await dp.start_polling(bot)

if __name__ == "__main__" :
    asyncio.run(main())
