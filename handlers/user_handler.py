import html
import os

from dotenv import load_dotenv
from aiogram import Router, types, F
from aiogram.filters import Command

from keyboards import inline_keyboards

user_router = Router()

load_dotenv()

BALANCE = os.getenv('BALANCE')

@user_router.callback_query(F.data == 'menu')
@user_router.message(Command('start'))
async def start(message):
    if isinstance(message, types.Message) and message.from_user: # то есть по идее канал может написать
        await message.answer(f'Добро пожаловать, <b>{html.escape(message.from_user.full_name)}</b>, ' 
                             'в финансовый помощник молодёжного служения A-life.' 
                             '\nВыберите, что вы хотели бы сделать:',
                             reply_markup=inline_keyboards.main_menu(), parse_mode='HTML')
    if isinstance(message, types.CallbackQuery) and isinstance(message.message, types.Message):
        await message.message.edit_text('Финансовый помощник молодёжного служения A-life.'
                                        '\nВыберите, что вы хотели бы сделать:',
                                        reply_markup=inline_keyboards.main_menu(), parse_mode='HTML')

@user_router.callback_query(F.data == 'Income')
async def income_handler(query: types.CallbackQuery):

    await query.answer(text="Обработано")

@user_router.callback_query(F.data == 'Show_All_Incomes')
async def show_income_handler(query: types.CallbackQuery):
    # Вывод в сообщении
    if isinstance(query.message, types.Message):
        final_text = 'Обработано'
        await query.message.edit_text(final_text, reply_markup=inline_keyboards.main_menu())

@user_router.callback_query(F.data == 'Balance')
async def balance_handler(query: types.CallbackQuery):
    
    await query.message.edit_text(text=f"Баланс: {BALANCE}", reply_markup=inline_keyboards.main_menu())

@user_router.callback_query(F.data == 'Expense')
async def expense_handler(query: types.CallbackQuery):
    await query.answer(text="Обработано", show_alert=True)

@user_router.callback_query(F.data == 'Show All Expenses')
async def show_expense_handler(query: types.CallbackQuery):
    await query.answer(text="Обработано")

# для сообщения по умолчанию
# @user_router.message()
# async def data_getting(message: types.Message):
#     await message.answer("Данные добавлены.")