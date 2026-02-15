from aiogram import Router, F
from aiogram.filters.command import CommandStart
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Message,
    CallbackQuery,
    ReplyKeyboardMarkup,
    KeyboardButton
)

from db.request import add_user, get_user_by_tg_id
from db.database import async_session_maker

router = Router()

inline_kb = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Регистрация", callback_data="register")]]
)

app_kb = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Открыть приложение", callback_data="open_app")]]
)

contact_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="📞 Отправить номер", request_contact=True)]],
    resize_keyboard=True,
    one_time_keyboard=True
)


# 🔹 Проверка регистрации
@router.message(CommandStart())
async def bot_start(message: Message):
    tg_id = message.from_user.id

    async with async_session_maker() as session:
        user = await get_user_by_tg_id(session, tg_id)

    if user:
        await message.answer(
            "Вы уже зарегистрированы 👍",
            reply_markup=app_kb
        )
    else:
        await message.answer(
            "Пройдите регистрацию, отправьте номер",
            reply_markup=inline_kb
        )


# 🔹 Кнопка регистрации
@router.callback_query(F.data == "register")
async def register_user(callback: CallbackQuery):
    await callback.message.answer(
        "Нажмите кнопку ниже, чтобы отправить номер",
        reply_markup=contact_kb
    )
    await callback.answer()


# 🔹 Получение контакта
@router.message(F.contact)
async def get_phone(message: Message):
    tg_id = message.from_user.id
    tg_name = message.from_user.full_name
    tg_username = message.from_user.username
    tg_number = message.contact.phone_number

    if message.contact.user_id != tg_id:
        await message.answer("Отправьте свой номер 😡")
        return

    # ✅ Создаём сессию вручную
    async with async_session_maker() as session:
        await add_user(
            session,
            tg_id,
            tg_number,
            tg_name,
            tg_username
        )

    await message.answer(
        "✅ Регистрация завершена",
        reply_markup=None
    )
