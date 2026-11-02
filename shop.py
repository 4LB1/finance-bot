import asyncio
import html
import aiosqlite

from aiogram import types, F, Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command, BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import TelegramObject

dp = Dispatcher()

admin_ids = [2054368848]

link = 'https://stepik.org/lesson/1007196/step/9?auth=registration&unit=1014951'

inline_kb = types.InlineKeyboardMarkup(inline_keyboard=[
    [types.InlineKeyboardButton(text='Каталог', callback_data='catalog')],
    [types.InlineKeyboardButton(text='Профиль', callback_data='profile'), types.InlineKeyboardButton(text='Тех. поддержка', url='t.me/wtf_slep')],
    [types.InlineKeyboardButton(text='O нас', callback_data='about')]
])

kb_0 = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text='Вернуться в меню', callback_data='menu')]
    ])

inline_kb_admin = types.InlineKeyboardMarkup(inline_keyboard=[
    [types.InlineKeyboardButton(text='Рассылка', callback_data='admin_newsletter')],
    [types.InlineKeyboardButton(text='Статистика', callback_data='admin_statistics')],
])

greeting_text = "Приветствуем в боте площадки Stepik."

async def add_user(user_id, full_name, username):
    connect = await aiosqlite.connect('bot_db1.db')
    cursor = await connect.cursor()
    user_check = await cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user_check = await user_check.fetchone()
    if user_check is None:
        await cursor.execute('INSERT INTO users (user_id, full_name, username) VALUES (?, ?, ?)', (user_id, full_name, username))
        await connect.commit()
    await cursor.close()
    await connect.close()

async def get_all_user_ids():
    connect = await aiosqlite.connect('bot_db1.db')
    cursor = await connect.cursor()
    all_ids = await cursor.execute('SELECT user_id FROM users')
    all_ids = await all_ids.fetchall()
    all_ids = [user_id[0] for user_id in all_ids]
    await cursor.close()
    await connect.close()
    return all_ids

class AdminState(StatesGroup):
    newsletter = State()

class IsAdmin(BaseFilter):
    async def __call__(self, obj: TelegramObject) -> bool:
        return obj..id in admin_ids


@dp.message(Command('admin'))
async def admin_handler(message: types.Message):
    await message.answer(greeting_text, reply_markup=inline_kb_admin)

async def get_user_count():
    connect = await aiosqlite.connect('bot_db1.db')
    cursor = await connect.cursor()
    user_count = await cursor.execute('SELECT COUNT(*) FROM users')
    user_count = await user_count.fetchone()
    await cursor.close()
    await connect.close()
    return user_count[0]

@dp.callback_query(F.data == 'admin_newsletter', IsAdmin())
async def admin_newsletter_handler(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text('Рассылка\n\nВведите сообщение, которое будет отправлено пользователям:')
    await state.set_state(AdminState.newsletter)

@dp.message(AdminState.newsletter)
async def admin_newsletter_message_handler(message: types.Message, state: FSMContext, bot: Bot):
    successful_sent_counter = 0
    failed_sent_counter = 0
    all_ids = await get_all_user_ids()
    for user_id in all_ids:
        try:
            await bot.send_message(user_id, message.text)
            await asyncio.sleep(0.2)
            successful_sent_counter +=1
        except Exception as e:
            failed_sent_counter +=1
    await state.clear()
    await message.answer(f'Результат отправки:\n\n Успешно: {successful_sent_counter}\nНе удалось отправить: {failed_sent_counter}', reply_markup=inline_kb_admin)

@dp.message(Command('get_data'))
async def get_data_handler(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    message_newsletter = user_data['message_newsletter']
    await message_newsletter.send_copy(message.from_user.id)

@dp.callback_query(F.data == 'admin_statistics')
async def admin_statistics_handler(call: types.CallbackQuery):
    user_count = await get_user_count()
    await call.message.edit_text(f'Статистика\n\nКоличество пользователей: {user_count}', reply_markup=kb_0)

@dp.callback_query(F.data == 'menu')
@dp.message(Command('start'))
async def start(message):
    await add_user(message.from_user.id, message.from_user.full_name, message.from_user.username)
    if isinstance(message, types.Message): await message.answer(f'Приветствуем <b><i>{html.escape(message.from_user.full_name)}</i></b> в тестовом боте', reply_markup=inline_kb, parse_mode='HTML')
    if isinstance(message, types.CallbackQuery) and isinstance(message.message, types.Message): await message.message.edit_text(f'Приветствуем <b>{html.escape(message.from_user.full_name)}</b> в тестовом боте', reply_markup=inline_kb, parse_mode='HTML')


@dp.callback_query(F.data == 'catalog')
async def catalog_handler(query: types.CallbackQuery):
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text='Курс по Python', url=link), types.InlineKeyboardButton(text='Курс по Aiogram', url=link)],
        [types.InlineKeyboardButton(text='Курс по Telebot', url=link), types.InlineKeyboardButton(text='Курс по Django', url=link)],
        [types.InlineKeyboardButton(text='Вернуться в меню', callback_data='menu')]
    ])
    if isinstance(query.message, types.Message): await query.message.edit_text('Ниже представлены курсы, доступные на платформе:', reply_markup=kb)

@dp.callback_query(F.data == 'profile')
async def profile_handler(query: types.CallbackQuery):
    if isinstance(query.message, types.Message): await query.message.edit_text(f'Имя пользователя: {query.from_user.first_name}\n Баланс: 500$', reply_markup=kb_0)

@dp.callback_query(F.data == 'about')
async def about_handler(query: types.CallbackQuery):
    if isinstance(query.message, types.Message): await query.message.edit_text('О нас:\nНичего не придумали, вот и думайте.', reply_markup=kb_0)

@dp.message()
async def unknown_handler(message: types.Message):
    await message.answer("Unknown doing", reply_markup=inline_kb)

async def main():
    await dp.start_polling(Bot("8310615846:AAEaKg57TT8IVmRm9DD00bxTWO3CV4PSQd4"), default=DefaultBotProperties(parse_mode='html'))

if __name__ == "__main__":
    asyncio.run(main())    