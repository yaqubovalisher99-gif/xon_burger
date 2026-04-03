import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

TOKEN = "TOKENINGNI_QO'Y"
ADMIN_ID = 123456789

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
    "baliq": [
        ("Kovirilgan baliq", 90000, "https://i.ytimg.com/vi/PO_t_lASSVA/maxresdefault.jpg"),
        ("Faliga baliq", 90000, "https://zira.uz/wp-content/uploads/2020/01/ryba-v-folge.jpg"),
        ("Setka baliq", 90000, "https://zira.uz/wp-content/uploads/2020/01/ryba-v-folge.jpg"),
    ],
    "issiq": [
        ("Bogir", 180000, "https://zira.uz/wp-content/uploads/2020/01/ryba-v-folge.jpg"),
        ("Bogir piyozli", 200000, "https://zira.uz/wp-content/uploads/2020/01/ryba-v-folge.jpg"),
        ("Ribay steyk", 60000, "https://zira.uz/wp-content/uploads/2020/01/ryba-v-folge.jpg"),
    ],
    "mangal": [
        ("Gijduvon", 17000, "https://zira.uz/wp-content/uploads/2020/01/ryba-v-folge.jpg"),
        ("Kuskavoy shashlik", 24000, "https://zira.uz/wp-content/uploads/2020/01/ryba-v-folge.jpg"),
    ],
    "xamir": [
        ("Gumma", 12000, "https://zira.uz/wp-content/uploads/2020/01/ryba-v-folge.jpg"),
        ("Tandir somsa", 12000, "https://zira.uz/wp-content/uploads/2020/01/ryba-v-folge.jpg"),
    ],
    "suyuq": [
        ("Mastava", 35000, "https://zira.uz/wp-content/uploads/2020/01/ryba-v-folge.jpg"),
        ("Tovuq sho'rva", 20000, "https://zira.uz/wp-content/uploads/2020/01/ryba-v-folge.jpg"),
    ],
    "ichimlik": [
        ("Kola 1.5L", 17000, "https://zira.uz/wp-content/uploads/2020/01/ryba-v-folge.jpg"),
        ("Fanta", 17000, "https://zira.uz/wp-content/uploads/2020/01/ryba-v-folge.jpg"),
    ],
    "araq": [
        ("Aroq 100gr", 10000, "https://zira.uz/wp-content/uploads/2020/01/ryba-v-folge.jpg"),
        ("Vino", 55000, "https://zira.uz/wp-content/uploads/2020/01/ryba-v-folge.jpg0"),
    ],
    "kaynak": [
        ("Uzbekistan 0.5L", 80000, "https://zira.uz/wp-content/uploads/2020/01/ryba-v-folge.jpg"),
    ],
    "pivo": [
        ("Tuborg", 17000, "https://zira.uz/wp-content/uploads/2020/01/ryba-v-folge.jpg"),
    ],
    "energetik": [
        ("Red Bull", 26000, "https://via.placeholder.com/300"),
    ],
    "podzakaz": [
        ("Manti", 15000, "https://zira.uz/wp-content/uploads/2020/01/ryba-v-folge.jpg"),
    ],
    "sheyx": [
        ("Sheyx joja", 60000, "https://zira.uz/wp-content/uploads/2020/01/ryba-v-folge.jpg"),
    ],
    "garnir": [
        ("Kartoshka fri", 10000, "https://zira.uz/wp-content/uploads/2020/01/ryba-v-folge.jpg"),
    ],
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
    await message.answer("Ismingizni kiriting:")
    await state.set_state(Register.name)

@dp.message(Register.name)
async def get_name(message: types.Message, state: FSMContext):
    users[message.from_user.id] = {"name": message.text}
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📞 Raqam yuborish", request_contact=True)]],
        resize_keyboard=True
    )
    await message.answer("Telefon yuboring:", reply_markup=kb)
    await state.set_state(Register.phone)

@dp.message(Register.phone)
async def get_phone(message: types.Message, state: FSMContext):
    users[message.from_user.id]["phone"] = message.contact.phone_number
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📍 Lokatsiya", request_location=True)]],
        resize_keyboard=True
    )
    await message.answer("Lokatsiya yuboring:", reply_markup=kb)
    await state.set_state(Register.location)

@dp.message(Register.location)
async def get_location(message: types.Message, state: FSMContext):
    users[message.from_user.id]["location"] = message.location
    await message.answer("Ro‘yxatdan o‘tdingiz!", reply_markup=main_menu())
    await state.clear()

# ================= CATEGORY =================
@dp.message(F.text == "🍔 Buyurtma berish")
async def category(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🐟 Baliq", callback_data="cat_baliq")],
        [InlineKeyboardButton(text="🍖 Issiq", callback_data="cat_issiq")],
        [InlineKeyboardButton(text="🔥 Mangal", callback_data="cat_mangal")],
        [InlineKeyboardButton(text="🥟 Xamir", callback_data="cat_xamir")],
        [InlineKeyboardButton(text="🍲 Suyuq", callback_data="cat_suyuq")],
        [InlineKeyboardButton(text="🥤 Ichimlik", callback_data="cat_ichimlik")],
        [InlineKeyboardButton(text="🍷 Aroq", callback_data="cat_araq")],
        [InlineKeyboardButton(text="🥃 Kaynak", callback_data="cat_kaynak")],
        [InlineKeyboardButton(text="🍺 Pivo", callback_data="cat_pivo")],
        [InlineKeyboardButton(text="⚡ Energetik", callback_data="cat_energetik")],
        [InlineKeyboardButton(text="📦 Pod zakaz", callback_data="cat_podzakaz")],
        [InlineKeyboardButton(text="👑 Sheyx", callback_data="cat_sheyx")],
        [InlineKeyboardButton(text="🍟 Garnir", callback_data="cat_garnir")],
    ])
    await message.answer("Kategoriya tanlang:", reply_markup=kb)

# ================= PRODUCTS =================
@dp.callback_query(F.data.startswith("cat_"))
async def show_products(callback: types.CallbackQuery):
    cat = callback.data.split("_")[1]
    for i, (name, price, img) in enumerate(products[cat]):
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🛒 Qo‘shish", callback_data=f"add_{cat}_{i}")]
            ]
        )
        await callback.message.answer_photo(
            photo=img,
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
    await callback.answer("Qo‘shildi ✅")

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
        text += f"{name} - {price}\n"
        total += price

    text += f"\n💰 Jami: {total}\n\nNon, choy, sous bilan yetkazamiz 😎"

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

    if not items:
        await callback.answer("Savatcha bo‘sh ❌")
        return

    text = f"Yangi buyurtma\n\n{user['name']}\n{user['phone']}\n\n"

    total = 0
    for name, price, _ in items:
        text += f"{name} - {price}\n"
        total += price

    text += f"\nJami: {total}"

    await bot.send_message(ADMIN_ID, text)

    loc = user['location']
    await bot.send_location(ADMIN_ID, loc.latitude, loc.longitude)

    cart[user_id] = []

    await callback.message.answer("Buyurtma yuborildi ✅")

# ================= RUN =================
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
