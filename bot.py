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

TOKEN = "7846933035:AAFNOW_BXt2oaVVDnE3yf1TqlAkXVxt6KJ0"
ADMIN_IDS = [5421038438, 8428945326,]

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
("Kovirilgan baliq", 90000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ14nKgXtK6q6C_kKe70-1bVBO7-vCMEiaegA&s"),
("Faliga baliq", 90000, "https://zira.uz/wp-content/uploads/2020/01/ryba-v-folge.jpg"),
("Setka baliq", 90000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTYP0XjPIambMEX9SqrfS2c9dYN_xcqAvnuCQ&s"),
],
"issiq": [
("Bog'ir", 180000, "https://i.ytimg.com/vi/_hIWWd6zIaQ/maxresdefault.jpg"),
("Bog'ir piyozli", 200000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRkS-bRQ1L10I5hqJjPk4NsL2y154u2MZ7_3Q&s"),
("Zamariq piyozli", 180000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQqS7zrC5FBu_ca7Ud7xHNW81q755AVaJ5Bnw&s"),
("Saryog dil", 340000, "https://data.daryo.uz/media/2024/04/09/921f8736466ff16ad692f72d1206790e-BypmIAWZ.jpeg"),
("Zigrik", 180000, "https://odam.uz/upload/media/entries/2017-08/18/1110-5-5fac3e595d0a8c2d556b3a04db11ce17.jpg"),
("Qo'y go'shti", 220000, "https://www.gazeta.uz/media/img/2023/02/U0iDU116754461950145_l.jpg"),
("Sho'r kabob bosh biqin", 220000, "https://i.ytimg.com/vi/rmT4iqeVDxU/maxresdefault.jpg"),
("Sho'r kabob son", 220000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcROlHAqooWJfWuLPuuY02j5LINbJVJL2LA8qg&s"),
("Saryog dil (1 port)", 85000, "https://data.daryo.uz/media/2024/04/09/921f8736466ff16ad692f72d1206790e-BypmIAWZ.jpeg"),
("Mol mushaki", 200000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ2mSqsIPseRkeD4pX3_mb6iYp1spEY-5jI1g&s"),
("Ribay steyk", 60000, "https://eda.rambler.ru/images/RecipePhoto/390x390/steyk-ribay-na-skovorode_175511_photo_183297.jpg"),
("Domashni katlet 150gr", 32000, "https://i.ytimg.com/vi/rpeW2MR86N8/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLDlSlI_j4L3cAC0zIzP7dGFdvIJ4Q"),
("Domashni katlet 100gr", 21000, "https://i.ytimg.com/vi/rpeW2MR86N8/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLDlSlI_j4L3cAC0zIzP7dGFdvIJ4Q"),
("Kabob asorti", 240000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSJvkg8rmlOBOUbRaiSZyTDHarmAb3SNNnLXg&s"),
("Qo'ziqorin kabob", 115000, "https://www.budgetbytes.com/wp-content/uploads/2025/07/Smoky-Sesame-Grilled-Mushroom-Kebabs-Macro.jpg"),
("Medalion 1kg", 280000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSlS_G8JwffTrx-UszyL767tu8R5ILYap3F5A&s"),
("Barra go'sht 1kg", 100000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRx2E2d6VhRpjuJp44VWTTSLTO402Gkf4tELg&s"),
("Mini asorti", 200000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRx2E2d6VhRpjuJp44VWTTSLTO402Gkf4tELg&s"),
("Asado qo'y bo'yin", 220000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT9-41wMMKAdXukBxVPheT6IcXeKOa6Bsu5og&s"),
("Saryog tovuq", 280000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQj0JoPcW1aoXXcKhB3ltW6DdmxWXN2k5kAZw&s"),
("Jo'ja", 60000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTttwjlDZRDXCJW8eVC4hmk-kRokkeQwlivyA&s"),
("Saryog tovuq (2)", 250000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQj0JoPcW1aoXXcKhB3ltW6DdmxWXN2k5kAZw&s"),
("Qaymoq kabob", 150000, "https://i.ytimg.com/vi/fAnr4ThhC1Q/sddefault.jpg"),
("Tushonka", 200000, "https://m.media-amazon.com/images/I/71UAGO-h9fL._AC_UF894,1000_QL80_.jpg"),
("Aprel kabob", 200000, "https://data.daryo.uz/media/cache/2020/10/Freepik-1-626x416.jpg"),
("Zamariq kabob", 115000, "https://www.cookingclassy.com/wp-content/uploads/2017/04/steak-kebabs-17.jpg"),
("Sho'r kabob piyozli", 250000, "https://i2.wp.com/highlandsranchfoodie.com/wp-content/uploads/2011/05/Lamb-Kabobs.jpg"),
("Barra go'sht 1kg (2)", 120000, "https://api.darakchi.uz/media/news_preview/2024/07/28/-_-85tluytfK-_w366Jn1vROmmN2wN4O-xl_zztfkIR_XkbQn1Q_NTyDdPK_LNSOwMB_0jfPQtF.medium.webp"),
("Pomidor qovurdoq", 100000, "https://havasfood.uz/wp-content/uploads/2020/12/zharennye-pomidory1-600x412.jpg"),
("Qo'y lapatka", 220000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTMPrvBTt8hWC0xXQ0VOGhlyG7r706_p5m0nQ&s"),
("Sirniy katlet", 40000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR3ZXczcyz8YPAnMGGOWdPO3cwQe55aF0k_WQ&s"),
],
"mangal": [
("G'ijduvon", 17000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRzpat8jMGKafN9ogtkwd4rlZn0ZCTc0wKzgw&s"),
("G'ijduvon katta", 25000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRzpat8jMGKafN9ogtkwd4rlZn0ZCTc0wKzgw&s"),
("Kuskavoy shashlik mol", 24000, "https://dostavo4ka.uz/upload-file/2021/07/05/6229/750x750-ffa8810e-46c4-4102-b141-00642a7285e4.jpg"),
("Urama kabob", 23000, "https://api.chaihana-minsk.by/wp-content/uploads/2019/09/%D0%A3%D1%80%D0%B0%D0%BC%D0%B0-%D0%BA%D0%B0%D0%B1%D0%BE%D0%B1-%D0%B8%D0%B7-%D0%B1%D0%B0%D1%80%D0%B0%D0%BD%D0%B8%D0%BD%D1%8B-%D0%A3%D1%80%D0%B0%D0%BC%D0%B0-%D0%BA%D0%B0%D0%B1%D0%BE%D0%B1-%D0%B8%D0%B7-%D0%B3%D0%BE%D0%B2%D1%8F%D0%B4%D0%B8%D0%BD%D1%8B-19-1024x684.jpg"),
("Bog'ir shashlik", 18000, "https://www.centralasia-travel.com/uploads/gallery/499/shashlik-05.jpg"),
("Sirniy katlet", 26000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR3ZXczcyz8YPAnMGGOWdPO3cwQe55aF0k_WQ&s"),
("Krilishka shashlik", 90000, "https://dostavo4ka.uz/upload-file/2021/07/05/6233/2c704cbe-db83-4f53-adf7-c0a0c965ff17.jpg"),
("Setka qovurga", 240000, "https://omnivorescookbook.com/wp-content/uploads/2016/07/1607_Xinjiang-Lamb-Skewer_006.jpg"),
("Setka kabob", 240000, "https://www.seriouseats.com/thmb/14Zpihnf3sr_0KvjIMeG86LyrWc=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/spicy-lamb-skewers-chinese-street-food-recipe-step-06-Collage-9c8c4dcbf8564abf9d211e1a9863d945.jpg"),
("Setka bag'ir", 18000, "https://i.ytimg.com/vi/yVzpfoD3UMA/sddefault.jpg"),
("Setka tovuq", 90000, "https://i.ytimg.com/vi/Jnf8eghBwxI/maxresdefault.jpg"),
("Kovurga setka", 240000, "https://www.shemins.com/wp-content/uploads/2025/07/BBQ-Lamb-Ribs-1200x675.jpg"),
("Shashlik asorti", 150000, "https://sochi.crazybrothers.ru/wp-content/uploads/Assorti-ljulja-kebab-1-ok-700x467.jpg"),
("Kuskavoy", 28000, "https://i.ytimg.com/vi/9YGFSDYmY_Y/sddefault.jpg"),
("Sirniy katlet katta", 90000, "https://s3-ap-south-1.amazonaws.com/betterbutterbucket-silver/mousumi-mandal20180810150342834.jpeg"),
("Sirniy katlet", 43000, "https://s3-ap-south-1.amazonaws.com/betterbutterbucket-silver/mousumi-mandal20180810150342834.jpeg"),
("KFC", 95000, "https://imageproxy.wolt.com/assets/67875f059573123c59b6db32"),
("Dumba", 24000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSTBJZm-Zqsp98na_hPdKI23V2wL9YDYUHRWA&s"),
("Qo'y steyk", 250000, "https://media-cdn.tripadvisor.com/media/photo-p/1c/62/02/3f/well-done.jpg"),
("Kavkaz shashlik", 110000, "https://www.chef.com.ua/userfiles/articles/small/1282812526_339.jpg"),
("Kavkaz qo'y", 80000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQqGkY_kVcFzh5_teYI8pRUuDVM3UzQQG1SJg&s"),
("Katlet", 18000, "https://i.ytimg.com/vi/t04zYXl2em4/maxresdefault.jpg"),
("Ovosh mangal", 50000, "https://e0.edimdoma.ru/data/recipes/0011/7620/117620-ed4_wide.jpg?1759197826"),
("Kovurga shashlik", 46000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRoQjoENcBpnN4GVkEvh3smUHl0sMQheDoi4A&s"),
("Vaguri 1kg", 240000, "https://www.restoran-shafran.uz/image/cache/catalog/product/mjasnie-bljuda/vaguri-iz-baranini-750x500.jpg"),
("Jaydari go'sht", 150000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSh7JfD3ZstkNbGQ3dseL_4-r_otpT3yNrl3A&s"),
("G'ijduvon 70gr", 11000, "https://i.ytimg.com/vi/jOl4c-u4TS0/mqdefault.jpg"),
("Jo'ja", 60000, "https://avatars.mds.yandex.net/get-altay/4544819/2a0000017769f8b8108760c9580a3ce55a7d/L_height"),
("Qo'y setka kabob", 200000, "https://grill-bbq.ru/wp-content/uploads/2018/11/steak-cowboy.jpg"),
("Xom go'sht", 150000, "https://tafseer-dreams.com/wp-content/uploads/2023/01/%D8%B1%D8%A4%D9%8A%D9%87-%D8%A7%D9%84%D9%84%D8%AD%D9%85-%D8%A7%D9%84%D9%86%D9%8A%D8%A1-%D9%81%D9%8A-%D8%A7%D9%84%D9%85%D9%86%D8%A7%D9%85-%D9%84%D9%84%D8%B9%D8%B2%D8%A8%D8%A7%D8%A1.jpg"),
("Barra go'sht", 120000, "https://oziqovqat.uz/uploads/products/5881/onWXNdDo79.jpg"),
("Kuskavoy pomidor", 25000, "https://oziqovqat.uz/uploads/products/5881/onWXNdDo79.jpg"),
("Krilcha shashlik", 14000, "https://grillmangal.com/cdn/shop/articles/1D3A8442.jpg?v=1728647798"),
],
"xamir": [
("Gumma", 12000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTVdW8eJN3gOprTo4_MvndyQWR9JClp3TH4RA&s"),
("Tuxum barak", 55000, "https://i.ytimg.com/vi/eA1-8TJxC9A/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLBpVb7OVhXLBoZvd5ltwLwtQzTtSw"),
("Kotr barak", 55000, "https://i.ytimg.com/vi/5moHorufT-w/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLCIRLTA8Kb_uvtdp0De-Q9phZgLSw"),
("Ko'k barak", 55000, "https://i.ytimg.com/vi/CLRxJacia_E/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLC8i0kI2ys-ho7ZxPU0vr46xrXIaA"),
("Turetskiy somsa", 7000, "https://media.ovkuse.ru/images/recipes/425de084-ed57-4eaf-9eb0-27fb60493917/425de084-ed57-4eaf-9eb0-27fb60493917.jpg"),
("Plimen", 35000, "https://i.ytimg.com/vi/YdLVhZmZGsI/hqdefault.jpg"),
("Kadi barak", 55000, "https://i.ytimg.com/vi/azTvFu93WLg/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLAR0fhjQ-SfAAb1uRYSq-ankzWfNA"),
("Kopshirma sirli", 1400, "https://zira.uz/wp-content/uploads/2018/01/hanum3-7-400x400.jpg"),
("Tandir somsa", 12000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSJo93EYsT-NUE5FJ5hkdW0jJjKwIBK-d2gMA&s"),
("Grechka", 40000, "https://i.ytimg.com/vi/mmdMEJLb4Qc/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLAOl_gqnrjkv2RSgjm7zYdXTGobIw"),
("Kartoshka barak", 55000, "https://i.ytimg.com/vi/tXpnB_cuv_Y/sddefault.jpg"),
("Barak asorti", 55000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRug2XuG5ZEnq_JAyKWqnw8C-WuMEdCP8DzxA&s"),
],
"suyuq": [
("Mastava", 35000, "https://images.gastronom.ru/rB504KSn0k4lnN8dxN9AMw3cseD32nUGUHnAF2yAoJo/pr:recipe-cover-image/g:ce/rs:auto:0:0:0/L2Ntcy9hbGwtaW1hZ2VzLzkxMzAzNjZmLWRkNDctNGNmYS05MDkyLTM2MmU4YzBjNmQ2ZC5qcGc.webp"),
("Tovuq sho'rva", 20000, "https://zira.uz/wp-content/uploads/2018/01/kurinyy-sup-s-ovoshhami.jpg"),
("Sho'rva osma", 40000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTetBPOSzJj2pLH0y-kSmtoVaQrFbGjahYVhw&s"),
("Sho'rva osma 0.5L", 25000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTetBPOSzJj2pLH0y-kSmtoVaQrFbGjahYVhw&s"),
("Unoshu", 30000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQqDexwo4UNouOwgD61Lwhp1__5YLNpfsU-eQ&s"),
("Unoshu 0.5L", 25000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQqDexwo4UNouOwgD61Lwhp1__5YLNpfsU-eQ&s"),
("Borsh", 40000, "https://images.gastronom.ru/meaxE0SX7mhX7ds3CQ6SQUHzpoYSkxuqV502y7XHMuk/pr:recipe-cover-image/g:ce/rs:auto:0:0:0/L2Ntcy9hbGwtaW1hZ2VzLzNiNzI1NDMzLTI5ZDQtNGZkZC1iMjYxLTBkM2MyMzg2NTYwYi5qcGc.webp"),
("Pelmen sho'rva", 35000, "https://i.ytimg.com/vi/zBd2HppSZXU/hqdefault.jpg"),
("Teftel sho'rva", 25000, "https://i.ytimg.com/vi/DiDaX8N893k/hq720.jpg?sqp=-oaymwE7CK4FEIIDSFryq4qpAy0IARUAAAAAGAElAADIQj0AgKJD8AEB-AH-CYAC0AWKAgwIABABGGUgTChKMA8=&rs=AOn4CLAK_Ir6FqwEfhDZ2PXbLZfNVzRIPw"),
("Unoshi chakida", 20000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQi1SoX0zYENuhpau99TJUkJG5lktn7GBOfAw&s"),
("Ko'za sho'rva", 30000, "https://i.ytimg.com/vi/iulx-vq4UlM/sddefault.jpg"),
("Chakida pelmen", 35000, "https://img.povar.ru/mobile/9d/9a/5b/5a/pelmeni_v_aerogrile-862792.jpg"),
],
"ichimlik": [
("Cola 1.5L", 17000, "https://images.uzum.uz/cia493tenntd8rfc2s40/original.jpg"),
("Fanta 1.5L", 17000, "https://images.uzum.uz/ce8a878v1htd23airm6g/original.jpg"),
("Pepsi 1.5L", 20000, "https://images.uzum.uz/d3fsp1oop562uss33s9g/original.jpg"),
("Chortoq", 8000, "https://cdn.bigmart.uz/file/hub/file/2025/4/17/2vrJyqENkzbgmnxaTdENHjxz44v.jpg"),
("Moxito", 12000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTjCuk9CrhbAyf0RM3IhcjP6zg1Zs3FRbVPHQ&s"),
("Borjomi", 20000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS7XrTTE6CZyc0EfKUdWBlMM--hIS1UIPSsOA&s"),
("Suv", 6000, "https://aniq.uz/photos/news/aBCeTZwbJWYs9kn.jpeg"),
("Ayron", 11000, "https://zira.uz/wp-content/uploads/2018/05/ayran-2.jpg"),
("Sharbat", 17000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRWeykj4SxiiR9v-d3FCI41zQytSTgSZGu3Zg&s"),
],
"aroq": [
("Aroq 100gr", 10000, "https://brooklyndrinks.uz/wp-content/uploads/2024/10/i-31.webp"),
("Vino", 55000, "https://saludconlupa.com/media/images/red-wine-pouring-from-bottle-glass.width-1920.jpg"),
("Karatov 0.5L", 45000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ4An1CQTR7ASjJpAp6P7FUmZfzdqoBcsQqzA&s"),
("Karatov 1L", 120000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ4An1CQTR7ASjJpAp6P7FUmZfzdqoBcsQqzA&s"),
("Shampan", 35000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRO9NMFJWySE5us_XZEqfSnYOIrbq1dHPFgjQ&s"),
("Chivas", 700000, "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Chivas_image_for_wikipedia.jpg/250px-Chivas_image_for_wikipedia.jpg"),
],
"kaynak": [
("Uzbekistan 0.5L", 80000, "https://www.cru.ru/upload/resize_cache/ram.watermark/cc7/b90/009/1089122/46907_2.webp"),
("Viskiy", 1100000, "https://complexbar.ru/images/blog/img/bokaly-dlya-viskiy-reiring.jpg?_t=1743155716"),
("Stareyshina", 600000, "https://butyl.shop/upload/iblock/465/17rgc1pa1gypuapftd55a7sdik6artew/87372c76_c1cc_11e6_8117_0cc47a1741cb_8457571f_f385_11eb_bba0_ac1f6b0311d9.resize1.png"),
],
"pivo": [
("Tuborg", 17000, "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Groen_Tuborg_bottles.jpg/330px-Groen_Tuborg_bottles.jpg"),
("Sarbast", 14000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTzMNCh7n-2exyYaPe9EwZuEvUCbCQwrYEC1w&s"),
("Baltika", 12000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS1jxRyVOalgyGUy5ouol2Z_3xu2qtm8UbXUw&s"),
("Heineken", 38000, "https://www.whitehorsewine.com/cdn/shop/products/WebGraphicEditor_38.png?v=1584724926"),
("Razlivnoy", 12000, "https://api.cabinet.smart-market.uz/uploads/images/ff8081815cbb21f8616637af"),
("Chips", 20000, "https://www.allrecipes.com/thmb/QO6I4DXnnrXZj1DjcOeRbFSmjk8=/0x512/filters:no_upscale():max_bytes(150000):strip_icc()/73135-homestyle-potato-chips-ddmfs-0348-3x4-hero-c21021303c8849bbb40c1007bfa9af6e.jpg"),
("Fistashka", 190000, "https://cdnn21.img.ria.ru/images/07e4/07/02/1573782611_0:136:3157:1912_1920x0_80_0_0_e5af34f7e12e8276027108aa03f79cdf.jpg"),
],
"energetik": [
("Flesh", 12000, "https://dostavo4ka.uz/upload-file/2021/05/05/493/c07a1652-3982-44aa-8eeb-37cc0820484c.jpg"),
("Gorilla", 15000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQu15yqVLDIx-r20UttkY8fGWCGf6JhxdYKBA&s"),
("Red Bull", 26000, "https://ir.ozone.ru/s3/multimedia-9/6337593537.jpg"),
("Adrenalin", 18000, "https://dostavo4ka.uz/upload-file/2021/05/05/1606/ee66ff62-3854-4e56-96af-dfc1afcece61.jpg"),
("Moxito", 40000, "https://ir.ozone.ru/s3/multimedia-v/c1000/6679245667.jpg"),
("Tarvuz sok", 10000, "https://i.ytimg.com/vi/_dOzuqwi84I/hq720.jpg?sqp=-oaymwE7CK4FEIIDSFryq4qpAy0IARUAAAAAGAElAADIQj0AgKJD8AEB-AH-CYAC0AWKAgwIABABGH8gICgTMA8=&rs=AOn4CLCfbJYlVkPVxB-uZ4VrtaTNGFAYPA"),
],
"podzakaz": [
("Lula kabob", 85000, "https://i.ytimg.com/vi/LTG7RzouUWw/sddefault.jpg"),
("Manti", 15000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSrxlZQON2wGPF1AMuTgYwSFv5R570ENcmvxw&s"),
("Kazak kabob", 220000, "https://cdn.nur.kz/images/1200x675/c293a36206b4a80e.jpeg?version=1"),
("Besh barmoq", 150000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSxWIkREcdjATHfUlgkvc-37qjP8o20MIN_-w&s"),
("Somsa", 8000, "https://safiabakery.uz/uploads/products/362_1715429417.jpg"),
("Golubsi", 80000, "https://shuba.life/static/content/thumbs/1824x912/1/c7/alqhaj---c2x1x50px50p-up--1c1117eddd1353fa98e874fd24afec71.jpg"),
("Julen", 110000, "https://i.ytimg.com/vi/yFONzifn-VI/hq720.jpg?sqp=-oaymwE7CK4FEIIDSFryq4qpAy0IARUAAAAAGAElAADIQj0AgKJD8AEB-AH-CYAC0AWKAgwIABABGFIgZSgPMA8=&rs=AOn4CLAPP-Sr7o_tG3U-2c7T1YzbdMoRZw"),
("Dimlama", 10000, "https://upload.wikimedia.org/wikipedia/commons/f/fd/Dimlama_%2816425713838%29.jpg"),
("Tobaka", 350000, "https://i.ytimg.com/vi/BVpAX57dZPo/mqdefault.jpg"),
],
"sheyx": [
("Sheyx kabob", 300000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQmhZUSZBUQ6q2lswUTUe0QcOqaG4J7r5TP5w&s"),
("Sheyx sho'r kabob", 220000, "https://www.allrecipes.com/thmb/nqBDLi0NrrYCm464cTH7jhxv9_I=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/8145753-5f66429f57af4a62aade3adf71dc28d3.jpg"),
("Sheyx mushak", 220000, "https://uzbekistan.travel/storage/app/media/Yuliya/Shashlik/cropped-images/shashlyk-assorti-toshkent-region-15-0-0-0-0-1603857618.jpg"),
("Sheyx setka", 240000, "https://dostavo4ka.uz/upload-file/2021/07/05/6227/750x750-df319789-2645-48f1-b2b6-c4f5ce6d14d6.jpg"),
("Sheyx sosiska", 160000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQOG1KF2QgniSRsc9VkCkpvbTP1RTLMPCT-Bg&s"),
("Sheyx jo'ja", 60000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTlW4hPN-_fvAz633jGv0P8G9NOz_RXcUvKaw&s"),
],
"garnir": [
("Fri", 10000, "https://pizzaking86.ru/wp-content/uploads/2021/12/kartofel-fri.jpg"),
("Pyure", 10000, "https://images.gastronom.ru/-BURK2Lb_b72n4Hiz_WQ6r32qBhFjnsgDItDP1-D4vc/pr:recipe-cover-image/g:ce/rs:auto:0:0:0/L2Ntcy9hbGwtaW1hZ2VzL2I3ZDAxMzM3LWUwZjQtNGY3YS1hZDFlLWQzZTQxZjk4YTkxMy5qcGc.webp"),
("Guruch", 5000, "https://storage.kun.uz/source/1/ED9jwMZn6aWplBfSGUbz3b1ocVnQ-2r9.jpg"),
("Qo'ziqorin", 150000, "https://zira.uz/wp-content/uploads/2018/02/kartoshka-gribi-3.jpg"),
("Pomidor", 25000, "https://img.freepik.com/premium-photo/tomato-cut-half-fresh-juicy-tomato-angle-is-straight-isolated_722504-859.jpg"),
("Kaymoq", 5000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR1tm_gLCzYNmyKZib6dSatuIoJHMhzR_z9Dg&s"),
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
    await message.answer("Ismingizni kiriting:")
    await state.set_state(Register.name)

@dp.message(Register.name)
async def get_name(message: types.Message, state: FSMContext):
    users[message.from_user.id] = {"name": message.text.title()}
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📞 Raqam yuborish", request_contact=True)]],
        resize_keyboard=True
    )
    await message.answer("Telefon yuboring:", reply_markup=kb)
    await state.set_state(Register.phone)

@dp.message(Register.phone)
async def get_phone(message: types.Message, state: FSMContext):
    if not message.contact:
        await message.answer("📞 Tugma orqali yubor!")
        return
    users[message.from_user.id]["phone"] = message.contact.phone_number
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📍 Lokatsiya", request_location=True)]],
        resize_keyboard=True
    )
    await message.answer("Lokatsiya yuboring:", reply_markup=kb)
    await state.set_state(Register.location)

@dp.message(Register.location)
async def get_location(message: types.Message, state: FSMContext):
    if not message.location:
        await message.answer("📍 Tugma orqali yubor!")
        return
    users[message.from_user.id]["location"] = message.location
    await message.answer("✅ Ro'yxatdan o'tdingiz!", reply_markup=main_menu())
    await state.clear()

# ================= CATEGORY =================
@dp.message(F.text == "🍔 Buyurtma berish")
async def category(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🐟 Baliq", callback_data="cat:baliq")],
        [InlineKeyboardButton(text="🍖 Issiq", callback_data="cat:issiq")],
        [InlineKeyboardButton(text="🔥 Mangal", callback_data="cat:mangal")],
        [InlineKeyboardButton(text="🥟 Xamir", callback_data="cat:xamir")],
        [InlineKeyboardButton(text="🍲 Suyuq", callback_data="cat:suyuq")],
        [InlineKeyboardButton(text="🥤 Ichimlik", callback_data="cat:ichimlik")],
        [InlineKeyboardButton(text="🍷 Aroq", callback_data="cat:aroq")],
        [InlineKeyboardButton(text="🥃 Kaynak", callback_data="cat:kaynak")],
        [InlineKeyboardButton(text="🍺 Pivo", callback_data="cat:pivo")],
        [InlineKeyboardButton(text="⚡ Energetik", callback_data="cat:energetik")],
        [InlineKeyboardButton(text="📦 Pod zakaz", callback_data="cat:podzakaz")],
        [InlineKeyboardButton(text="👑 Sheyx", callback_data="cat:sheyx")],
        [InlineKeyboardButton(text="🍟 Garnir", callback_data="cat:garnir")],
    ])
    await message.answer("👇 Tanlang:", reply_markup=kb)

# ================= SHOW PRODUCTS =================
@dp.callback_query(F.data.startswith("cat:"))
async def show_products(callback: types.CallbackQuery):
    await callback.answer()
    cat = callback.data.split(":")[1]

    if cat not in products:
        await callback.message.answer("❌ Topilmadi")
        return

    for i, (name, price, img) in enumerate(products[cat]):
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🛒 Qo'shish", callback_data=f"add|{cat}|{i}")]
            ]
        )
        await callback.message.answer_photo(
            photo=img,
            caption=f"{name}\n💰 {price} so'm",
            reply_markup=kb
        )

# ================= ADD TO CART =================
@dp.callback_query(F.data.startswith("add|"))
async def add_to_cart(callback: types.CallbackQuery):
    await callback.answer("✅ Savatga qo'shildi!")
    user_id = callback.from_user.id
    _, cat, i = callback.data.split("|")

    if cat not in products:
        return

    item = products[cat][int(i)]
    cart.setdefault(user_id, []).append(item)

# ================= SHOW CART =================
@dp.message(F.text == "🛒 Savatcha")
async def show_cart(message: types.Message):
    user_id = message.from_user.id
    items = cart.get(user_id, [])

    if not items:
        await message.answer("🛒 Savatcha bo'sh ❌")
        return

    text = "🛒 SAVATCHA:\n\n"
    total = 0

    for i, (name, price, _) in enumerate(items, 1):
        text += f"{i}. {name} - {price} so'm\n"
        total += price

    text += f"\n{'='*30}\n"
    text += f"💰 JAMI: {total} so'm\n"
    text += f"{'='*30}\n\n"
    text += "🚚 Dastavka hizmati mavjud!\n"

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📦 Buyurtma berish", callback_data="order")],
            [InlineKeyboardButton(text="◀️ Orqaga", callback_data="back_menu")]
        ]
    )

    await message.answer(text, reply_markup=kb)

# ================= BACK TO MENU =================
@dp.callback_query(F.data == "back_menu")
async def back_menu(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer("👇 Tanlang:", reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🐟 Baliq", callback_data="cat:baliq")],
        [InlineKeyboardButton(text="🍖 Issiq", callback_data="cat:issiq")],
        [InlineKeyboardButton(text="🔥 Mangal", callback_data="cat:mangal")],
        [InlineKeyboardButton(text="🥟 Xamir", callback_data="cat:xamir")],
        [InlineKeyboardButton(text="🍲 Suyuq", callback_data="cat:suyuq")],
        [InlineKeyboardButton(text="🥤 Ichimlik", callback_data="cat:ichimlik")],
        [InlineKeyboardButton(text="🍷 Aroq", callback_data="cat:aroq")],
        [InlineKeyboardButton(text="🥃 Kaynak", callback_data="cat:kaynak")],
        [InlineKeyboardButton(text="🍺 Pivo", callback_data="cat:pivo")],
        [InlineKeyboardButton(text="⚡ Energetik", callback_data="cat:energetik")],
        [InlineKeyboardButton(text="📦 Pod zakaz", callback_data="cat:podzakaz")],
        [InlineKeyboardButton(text="👑 Sheyx", callback_data="cat:sheyx")],
        [InlineKeyboardButton(text="🍟 Garnir", callback_data="cat:garnir")],
    ]))

# ================= ORDER =================
@dp.callback_query(F.data == "order")
async def order(callback: types.CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id

    if user_id not in users:
        await callback.message.answer("❌ Avval /start bosing")
        return

    items = cart.get(user_id, [])
    if not items:
        await callback.message.answer("❌ Savatcha bo'sh")
        return

    user = users[user_id]

    text = f"🧾 YANGI BUYURTMA\n\n"
    text += f"👤 Ism: {user['name']}\n"
    text += f"📞 Tel: {user['phone']}\n\n"
    text += f"📦 MAHSULOTLAR:\n"
    text += f"{'='*30}\n"

    total = 0
    for i, (name, price, _) in enumerate(items, 1):
        text += f"{i}. {name} - {price} so'm\n"
        total += price

    text += f"{'='*30}\n"
    text += f"💰 JAMI: {total} so'm\n"
    text += f"🚚 Dastavka hizmati mavjud!\n"

    loc = user['location']

    for admin in ADMIN_IDS:
        await bot.send_message(admin, text)
        await bot.send_location(admin, loc.latitude, loc.longitude)

    cart[user_id] = []

    await callback.message.answer("✅ Buyurtma yuborildi! Tez orada siz bilan bog'lanamiz.")
    await callback.message.answer("Raxmat, buyurtma berganingiz uchun! 🙏", reply_markup=main_menu())

# ================= RUN =================
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
