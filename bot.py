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
        ("🍔 Kartoshka Fri", 15000, "https://t4.ftcdn.net/jpg/05/85/29/13/360_F_585291338_0J8Q8vYbKDCu8yqqwAO8PsQZ4ESP2zd8.jpg"),
        ("🍔 SHashlik", 15000, "https://t4.ftcdn.net/jpg/05/85/29/13/360_F_585291338_0J8Q8vYbKDCu8yqqwAO8PsQZ4ESP2zd8.jpg"),
        ("🍔 Naggetsi", 80000, "https://t4.ftcdn.net/jpg/05/85/29/13/360_F_585291338_0J8Q8vYbKDCu8yqqwAO8PsQZ4ESP2zd8.jpg"),
        ("🍔 Xan Burger", 40000, "https://t4.ftcdn.net/jpg/05/85/29/13/360_F_585291338_0J8Q8vYbKDCu8yqqwAO8PsQZ4ESP2zd8.jpg"),
        ("🍔 Ufo Burger", 35000, "https://static.vecteezy.com/system/resources/thumbnails/056/438/079/small/high-quality-transparent-background-black-burger-image-for-branding-and-ads-png.png"),
        ("🍔 Cheeseburger", 35000, "https://images.themodernproper.com/production/posts/2016/ClassicCheeseBurger_9.jpg?w=960&h=960&q=82&fm=jpg&fit=crop&dm=1749310239&s=603ff206b8a47f03f208a894e0667621"),
        ("🍔 Non Kabob", 35000, "https://avatars.mds.yandex.net/get-altay/6302373/2a0000017f278e3c10194a4c570c1f43b17e/L_height"), 
        ("🍔 Gamburger", 15000, "https://avatars.mds.yandex.net/get-altay/6302373/2a0000017f278e3c10194a4c570c1f43b17e/L_height"),
        ("🍔 Patira Gamburger", 35000, "https://avatars.mds.yandex.net/get-altay/6302373/2a0000017f278e3c10194a4c570c1f43b17e/L_height"),
        ("🍔 Xot Dog", 18000, "https://avatars.mds.yandex.net/get-altay/6302373/2a0000017f278e3c10194a4c570c1f43b17e/L_height"),
        ("🍔 Xot Dog Dvaynoy", 20000, "https://avatars.mds.yandex.net/get-altay/6302373/2a0000017f278e3c10194a4c570c1f43b17e/L_height"),
        ("🍔 Xot Dog Qatlet", 25000, "https://avatars.mds.yandex.net/get-altay/6302373/2a0000017f278e3c10194a4c570c1f43b17e/L_height"),
        ("🍔 Xot Dog Go'sht", 25000, "https://avatars.mds.yandex.net/get-altay/6302373/2a0000017f278e3c10194a4c570c1f43b17e/L_height"),
    ],
    "lavash": [
        ("🌯 Pite Lavash", 35000, "https://avatars.mds.yandex.net/get-altay/5098810/2a00000182009c9f9161f1d17565bd553ae2/L_height"),
        ("🌯 Lavash", 35000, "https://avatars.mds.yandex.net/get-altay/5098810/2a00000182009c9f9161f1d17565bd553ae2/L_height"),
        ("🌯 Patir Lavash", 35000, "https://avatars.mds.yandex.net/get-altay/5098810/2a00000182009c9f9161f1d17565bd553ae2/L_height"),
        ("🌯 Lavash Dvaynoy", 45000, "https://cdn.foodpicasso.com/assets/07/9b/39/f4/079b39f4a3a42da172fe111fd5233473---png_1000x_103c0_convert.png"),
        ("🧀 Lavash sir", 35000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ3RkSYUINIJlIEYWgUoYgCxByWap73QZc2-A&s"),
        ("🌶 Lavash o‘tkir", 35000, "https://cdn.delever.uz/delever/16f04863-7c42-467d-bf78-2c53db5385f0"),
        ("🌯 Donar", 40000, "https://ce6e1bcc-e329-4500-b965-54d06a22bcc8.selstorage.ru/4538923/93351e97-58c2-4053-9759-bd0837e243e2.jpg"),
        ("🌯 Haggi", 35000, "https://www.restoran-shafran.uz/image/cache/catalog/product/haggi-2-750x500.jpg"),
        ("🍔 Somsa", 15000, "https://avatars.mds.yandex.net/get-altay/6302373/2a0000017f278e3c10194a4c570c1f43b17e/L_height"),
    ],
    "drink": [
        ("🥤 Cola 0.5L", 8000, "https://positano.lv/wp-content/uploads/2019/03/cola-zero-0.5-new.png"),
        ("🥤 Cola 1L", 12000, "https://www.freeiconspng.com/uploads/coca-cola-bottle-png--1.png"),
        ("🥤 Fanta", 12000, "https://yastatic.net/avatars/get-grocery-goods/2888787/cb6e0aca-7b69-4689-87fa-0790760892f8/500x500-orig"),
        ("🥤 Moxito", 20000, "https://yastatic.net/avatars/get-grocery-goods/2888787/cb6e0aca-7b69-4689-87fa-0790760892f8/500x500-orig"),
        ("🥤 Kakteyl(Milksheyk)", 20000, "https://yastatic.net/avatars/get-grocery-goods/2888787/cb6e0aca-7b69-4689-87fa-0790760892f8/500x500-orig"),
        ("🥤 Kakteyl Banan", 20000, "https://yastatic.net/avatars/get-grocery-goods/2888787/cb6e0aca-7b69-4689-87fa-0790760892f8/500x500-orig"),
        ("🥤 Kakteyl Qulupnay", 20000, "https://yastatic.net/avatars/get-grocery-goods/2888787/cb6e0aca-7b69-4689-87fa-0790760892f8/500x500-orig"),
        ("🥤 Kakteyl Kiwi", 20000, "https://yastatic.net/avatars/get-grocery-goods/2888787/cb6e0aca-7b69-4689-87fa-0790760892f8/500x500-orig"),
    ],
    "Setlarimiz":[
        ("🍔 1 Setimiz 2ta burger 1 kola kartoshka fri 2ta sous", 99000, "https://avatars.mds.yandex.net/get-altay/6302373/2a0000017f278e3c10194a4c570c1f43b17e/L_height"),
        ("🍔 2 Setimiz 2ta lavash 1 kola kartoshka fri 2ta sous", 99000, "https://avatars.mds.yandex.net/get-altay/6302373/2a0000017f278e3c10194a4c570c1f43b17e/L_height"),
        ("🍔 3 Setimiz 1kg steyk 4ta shashlik 2/4 katlet kartoshka fri  4ta sous 1cola non", 250000, "https://avatars.mds.yandex.net/get-altay/6302373/2a0000017f278e3c10194a4c570c1f43b17e/L_height"),    
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
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🛒 Qo‘shish",
                        callback_data=f"add_{cat}_{i}"
                    )
                ]
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
