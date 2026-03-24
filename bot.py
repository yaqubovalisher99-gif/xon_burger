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
        ("🍔 Kartoshka Fri", 15000, "https://tiktak-delivery.ru/img/dish/LjNSL6Y1ZkEC3B2k.jpg?mark=%2Fhome%2Ftiktak%2Fhtdocs%2Fpublic%2Fassets%2Findex%2Fimages%2Fwater-mark-2.png&s=235f279c3ce2e184a6dfbd3a3f049417"),
        ("🍔 SHashlik", 15000, "https://uzbekistan.travel/storage/app/media/Yuliya/Shashlik/cropped-images/gizhduanskiy-shashlyk-62-0-0-0-0-1603857586.jpg"),
        ("🍔 Naggetsi", 80000, "https://avatars.mds.yandex.net/get-vertis-journal/4465444/b17e81fc-17c7-4ff9-b0b6-03566710b1aa.jpg/1600x1600"),
        ("🍔 Xan Burger", 40000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQW0TN2RswEQWCH7Tm0BoNyXkhJ-fJshQ7BDw&s"),
        ("🍔 Ufo Burger", 35000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQcjc5C-J7nn3Fmg3hNMgfGAhFvFqZaR6upmQ&s"),
        ("🍔 Cheeseburger", 35000, "https://www.sargento.com/assets/Uploads/Recipe/Image/burger_0__FocusFillWyIwLjAwIiwiMC4wMCIsODAwLDQ3OF0_CompressedW10.jpg"),
        ("🍔 Non Kabob", 35000, "https://w7.pngwing.com/pngs/106/531/png-transparent-doner-kebab-hamburger-zapiekanka-restaurant-meat-food-beef-recipe-thumbnail.png"), 
        ("🍔 Gamburger", 15000, "https://www.instagram.com/reel/DU2bTLzjAML/"),
        ("🍔 Patira Gamburger", 35000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRPmYJqjjF7E-B-hLJdyG1ub3SwavU7-8htLWXBEquT0pjkfi_o"),
        ("🍔 Xot Dog", 18000, "https://i.ytimg.com/vi/WdBswbdm1Yo/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLA4hW1Evt0plB3c7pdGUNOBMM7ITg"),
        ("🍔 Xot Dog Dvaynoy", 20000, "https://media.ovkuse.ru/images/recipes/333ace94-b781-4cb9-893e-c2aa44f9544f/333ace94-b781-4cb9-893e-c2aa44f9544f_420_420.webp"),
        ("🍔 Xot Dog Qatlet", 25000, "https://i.ytimg.com/vi/clXywwZ6SmM/maxresdefault.jpg"),
        ("🍔 Xot Dog Go'sht", 25000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRIKISvW1AbvcPXMxd5ms9coWX_0B4itLIEuA&s"),
    ],
    "lavash": [
        ("🌯 Pite Lavash", 35000, "https://i.ytimg.com/vi/coGxjpPgF0M/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLCcXa4xgC6ES_RxVuczDrery0QoEw"),
        ("🌯 Lavash", 35000, "https://data.daryo.uz/media/cache/2020/05/Lavash-1000x667.jpg"),
        ("🌯 Patir Lavash", 35000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTFEjOFvSmjhhuUKtFrlpGZft-gaC3B4zEWJQ&s"),
        ("🌯 Lavash Dvaynoy", 45000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTOnzEjuZXRA1xkSYNbxbRXrgF8wPtm2f_kLg&s"),
        ("🧀 Lavash sir", 35000, "https://maxway.uz/_next/image?url=https%3A%2F%2Fcdn.delever.uz%2Fdelever%2F174ded8b-61f0-4e75-91fb-e9639332b80a&w=3840&q=75"),
        ("🌶 Lavash o‘tkir", 35000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTfP48wCGSwSKij0RH-owZ0xZJ-Btl49wFzJw&s"),
        ("🌯 Donar", 40000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRzw3nmA8AxjraTSjtE02b9hKR8ZGrf7Asgfg&s"),
        ("🌯 Haggi", 35000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSNLb5Vf1QphJUx0IozziUtuCaxGSBPrK7X8w&s"),
        ("🍔 Somsa", 15000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ-Ie-JpMEhbJ_snmq_PsMHdnLIxtYGjEtn0g&s"),
    ],
    "drink": [
        ("🥤 Cola 0.5L", 8000, "https://positano.lv/wp-content/uploads/2019/03/cola-zero-0.5-new.png"),
        ("🥤 Cola 1L", 12000, "https://www.freeiconspng.com/uploads/coca-cola-bottle-png--1.png"),
        ("🥤 Fanta", 12000, "https://yastatic.net/avatars/get-grocery-goods/2888787/cb6e0aca-7b69-4689-87fa-0790760892f8/500x500-orig"),
        ("🥤 Moxito", 20000, "https://img.freepik.com/free-photo/traditional-mojito-with-ice-mint-table_140725-867.jpg?semt=ais_hybrid&w=740&q=80"),
        ("🥤 Kakteyl Banan", 20000, "https://yastatic.net/avatars/get-grocery-goods/2888787/cb6e0aca-7b69-4689-87fa-0790760892f8/500x500-orig"),
        ("🥤 Kakteyl Qulupnay", 20000, "https://chatgpt.com/backend-api/estuary/content?id=file_0000000026b071fd850717ad91e51e24&ts=492881&p=fs&cid=1&sig=5e6d5cffff6f32de044b9cffc2ba9816beca8bc47b0ac5766e9e23e56d1364fe&v=0"),
        ("🥤 Kakteyl Kiwi", 20000, "https://chatgpt.com/backend-api/estuary/content?id=file_00000000ebc071fdb1af3e55feb63a05&ts=492881&p=fs&cid=1&sig=b55b6ebd33e868ef109084fbaadfb43cd4488a91985022eb3762816da19e7b85&v=0"),
    ],
    "Setlarimiz":[
        ("🍔 1 Setimiz 2ta burger 1 kola kartoshka fri 2ta sous", 99000, "https://chatgpt.com/backend-api/estuary/content?id=file_000000000e3471fd84889042b515c318&ts=492881&p=fs&cid=1&sig=cdb87320eb9ba114ab71ae552e6e95d7f916f187a2a208ccc781dc1274ea542b&v=0"),
        ("🍔 2 Setimiz 2ta lavash 1 kola kartoshka fri 2ta sous", 99000, "https://www.instagram.com/reel/DU-JYr9iGkS/"),
        ("🍔 3 Setimiz 1kg steyk 4ta shashlik 2/4 katlet kartoshka fri  4ta sous 1cola non", 250000, "https://chatgpt.com/backend-api/estuary/content?id=file_000000000d4871fda72f1f4d66105bc2&ts=492881&p=fs&cid=1&sig=60878cefa37d68996e965f5f65ee0d16c0b3aba0ed2551f924411177ab3b5e01&v=0"),    
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
        [InlineKeyboardButton(text="🥤 Ichimlik", callback_data="cat_drink")],
        [InlineKeyboardButton(text="🔥 Setlarimiz", callback_data="cat_Setlarimiz")]
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
