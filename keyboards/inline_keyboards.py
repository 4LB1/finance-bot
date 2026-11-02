from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton

def main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Доход", callback_data="Income"),
            InlineKeyboardButton(text="Расход", callback_data="Expense")
        ],
        [
            InlineKeyboardButton(text="Баланс", callback_data="Balance"),
            InlineKeyboardButton(text="Розница", callback_data="Cash_Flow")
        ],
        [
            InlineKeyboardButton(text="История доход", callback_data="Show_All_Incomes"),
            InlineKeyboardButton(text="История расход", callback_data="Show All Expenses")
        ]
        ])

def back_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Вернуться', callback_data='menu')
        ]
    ])

