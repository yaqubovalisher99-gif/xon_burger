import asyncio
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

TOKEN = "8046143748:AAFXa822qHNKrJVs-LIVarwA0XQTaLLhn9w"
ADMIN_ID = 5825744781

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# ================= STATE =================
class Register(StatesGroup):
    name = State()
    phone = State()
    location = State()

users = {}
cart = {}

# ================= PRODUCTS =================
products = {
    "burger": [
        ("🍔 Xan Burger", 45000, "images/xan_burger.jpg"),
        ("🍔 Black Burger", 40000, "images/black_burger.png"),
        ("🍔 Cheeseburger", 35000, "images/cheese_burger.png"),
        ("🍔 Gamburger", 16000, "images/gamburger.jpg"),
    ],
    "lavash": [
        ("🌯 Lavash", 35000, "images/lavash.jpg"),
        ("🌯 Lavash 2x", 50000, "images/lavash_2x.jpg"),
        ("🧀 Lavash sir", 40000, "images/sirli_lavash.jpg"),
        ("🌶 Lavash o‘tkir", 38000, "images/achchi_lavash.png"),
        ("🌯 Donar", 50000, "images/donar.jpg"),
        ("🌯 Haggi", 40000, "images/haggi.jpg"),
    ],
    "drink": [
        ("🥤 Cola 0.5L", 8000, "images/cola_05.png"),
        ("🥤 Cola 1L", 12000, "images/cola_1l.png"),
        ("🥤 Fanta", 10000, "images/fanta_1l.png"),
    ]
}

# ================= MENU =================
def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🍔 Buyurtma berish")],
            [KeyboardButton(text="🛒 Savatcha")]
        ],
        resize_keyboard=True
    )

# ================= START =================
@dp.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    await message.answer("👤 Ismingizni kiriting:")
    await state.set_state(Register.name)

@dp.message(Register.name)
async def get_name(message: types.Message, state: FSMContext):
    users[message.from_user.id] = {"name": message.text}

    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📞 Raqam yuborish", request_contact=True)]],
        resize_keyboard=True
    )

    await message.answer("📞 Telefon yuboring:", reply_markup=kb)
    await state.set_state(Register.phone)

@dp.message(Register.phone)
async def get_phone(message: types.Message, state: FSMContext):
    users[message.from_user.id]["phone"] = message.contact.phone_number

    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📍 Lokatsiya", request_location=True)]],
        resize_keyboard=True
    )

    await message.answer("📍 Lokatsiya yuboring:", reply_markup=kb)
    await state.set_state(Register.location)

@dp.message(Register.location)
async def get_location(message: types.Message, state: FSMContext):
    users[message.from_user.id]["location"] = message.location

    await message.answer("✅ Ro‘yxatdan o‘tdingiz!", reply_markup=main_menu())
    await state.clear()

# ================= CATEGORY =================
@dp.message(F.text == "🍔 Buyurtma berish")
async def category(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🍔 Burger", callback_data="cat_burger")],
        [InlineKeyboardButton(text="🌯 Lavash", callback_data="cat_lavash")],
        [InlineKeyboardButton(text="🥤 Ichimlik", callback_data="cat_drink")]
    ])
    await message.answer("Kategoriya tanlang:", reply_markup=kb)

# ================= PRODUCTS =================
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

@dp.callback_query(F.data.startswith("cat_"))
async def show_products(callback: types.CallbackQuery):
    await callback.answer()

    cat = callback.data.split("_")[1]

    for i, (name, price, img) in enumerate(products[cat]):
        photo = FSInputFile(str(BASE_DIR / img))

        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="🛒 Qo‘shish",
                callback_data=f"add_{cat}_{i}"
            )]
        ])

        await callback.message.answer_photo(
            photo=photo,
            caption=f"{name} - {price} so‘m",
            reply_markup=kb
        )
# ================= ADD =================
@dp.callback_query(F.data.startswith("add_"))
async def add(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    _, cat, i = callback.data.split("_")

    item = products[cat][int(i)]

    cart.setdefault(user_id, []).append(item)

    await callback.answer("Savatchaga qo‘shildi ✅")

# ================= CART =================
@dp.message(F.text == "🛒 Savatcha")
async def show_cart(message: types.Message):
    user_id = message.from_user.id
    items = cart.get(user_id, [])

    if not items:
        await message.answer("Savatcha bo‘sh ❌")
        return

    text = "🛒 Savatcha:\n\n"
    total = 0

    for name, price, _ in items:
        text += f"{name} - {price} so‘m\n"
        total += price

    text += f"\n💰 Jami: {total}"

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📦 Buyurtma berish", callback_data="order")]
    ])

    await message.answer(text, reply_markup=kb)

# ================= ORDER =================
@dp.callback_query(F.data == "order")
async def send_order(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user = users.get(user_id)
    items = cart.get(user_id, [])

    text = f"📦 Yangi buyurtma\n\n👤 {user['name']}\n📞 {user['phone']}\n\n"

    total = 0
    for name, price, _ in items:
        text += f"{name} - {price}\n"
        total += price

    text += f"\n💰 Jami: {total}"

    await bot.send_message(ADMIN_ID, text)

    # 📍 lokatsiya yuborish
    loc = user['location']
    await bot.send_location(ADMIN_ID, latitude=loc.latitude, longitude=loc.longitude)

    cart[user_id] = []
    await callback.message.answer("✅ Buyurtma yuborildi!")

# ================= RUN =================
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
