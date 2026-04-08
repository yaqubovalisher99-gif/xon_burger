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
ADMIN_IDS = [5421038438, 8428945326,5825744781,]

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
"issiq": [
("Tobaqa domashniy saryogo", 250000, ""),
("Tobaqa bruller saryogo", 85000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRkS-bRQ1L10I5hqJjPk4NsL2y154u2MZ7_3Q&s"),
("Saryogo juja", 60000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQqS7zrC5FBu_ca7Ud7xHNW81q755AVaJ5Bnw&s"),
("Shor kabob pomidor sousli", 230000, "https://www.russianfood.com/dycontent/images_upl/541/big_540774.jpg"),
("Shor kabob pomidor sousli 0.5kg", 1150000, "https://www.russianfood.com/dycontent/images_upl/541/big_540774.jpg"),
("Shor kabob 1kg", 220000, "https://odam.uz/upload/media/entries/2017-08/18/1110-5-5fac3e595d0a8c2d556b3a04db11ce17.jpg"),
("Shor kabob 0.5kg", 110000, "https://odam.uz/upload/media/entries/2017-08/18/1110-5-5fac3e595d0a8c2d556b3a04db11ce17.jpg"),
("Tishonka 1kg", 190000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSU66-qnfe7PBbaJnTGGxx8VqdHYIYrZpXb2Q&s"),
("Tishonka 0.5kg", 80000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSU66-qnfe7PBbaJnTGGxx8VqdHYIYrZpXb2Q&s"),
("Zigrik 1kg", 180000, "https://i.ytimg.com/vi/Nnwi2XXv9bg/maxresdefault.jpg"),
("Zigrik 0.5kg", 180000, "https://i.ytimg.com/vi/Nnwi2XXv9bg/maxresdefault.jpg"),
("Saryog dil (1 port)", 85000, "https://i.ytimg.com/vi/p0miMlI7OAs/maxresdefault.jpg"),
("Mol mushaki", 220000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ4Z7lYMSML_vSBM0aARyvlVAtERISZ4Z2cNA&s"),
("Qozi goshti qazon kabob", 220000, "https://eda.rambler.ru/images/RecipePhoto/390x390/steyk-ribay-na-skovorode_175511_photo_183297.jpg"),
("Zamariq kabob 1porsi", 115000, "https://i.ytimg.com/vi/rpeW2MR86N8/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLDlSlI_j4L3cAC0zIzP7dGFdvIJ4Q"),
("Qaymoq kabob 1porsi", 150000, "https://i.ytimg.com/vi/rpeW2MR86N8/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLDlSlI_j4L3cAC0zIzP7dGFdvIJ4Q"),
("Say kabob 1porsi", 95000, "https://dyj6gt4964deb.cloudfront.net/images/crop-9a5b59b6-9776-4889-a443-2c08032bb7f3.jpeg"),
("Medalion", 280000, "https://6666beef.com/cdn/shop/files/Tenderloin-Medallions_0002_Cooked-02-web.jpg?v=1730587632&width=990"),
("Mesniy xoroz chehambel", 350000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSlS_G8JwffTrx-UszyL767tu8R5ILYap3F5A&s"),
("Kabob asorti 1kg", 250000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRx2E2d6VhRpjuJp44VWTTSLTO402Gkf4tELg&s"),
("Juli 1 porsi", 100000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRx2E2d6VhRpjuJp44VWTTSLTO402Gkf4tELg&s"),
("Bogir 1kg", 180000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT9-41wMMKAdXukBxVPheT6IcXeKOa6Bsu5og&s"),
],
"mangal": [
("G'ijduvon shashlik", 17000, "https://i.ytimg.com/vi/aBC4gTWbBiU/maxresdefault.jpg"),
("G'ijduvon katta shashlik", 25500, "https://uzbekistan.travel/storage/app/media/nargiza/cropped-images/shashlik2-0-0-0-0-1588924572.jpg"),
("Kuskavoy shashlik mol", 25000, "https://dostavo4ka.uz/upload-file/2021/07/05/6227/750x750-df319789-2645-48f1-b2b6-c4f5ce6d14d6.jpg"),
("Kuskavoy shashlik qoy", 28000, "https://i.ytimg.com/vi/6GCe_xxk0pM/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLAZ_MsmpVmsSyEyLvUEbqspRr8Jow"),
("Dumba qoy", 25000, "https://www.centralasia-travel.com/uploads/gallery/499/shashlik-05.jpg"),
("Setka kabob 1kg", 240000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR3ZXczcyz8YPAnMGGOWdPO3cwQe55aF0k_WQ&s"),
("Setka kovurga qoy", 240000, "https://dostavo4ka.uz/upload-file/2021/07/05/6233/2c704cbe-db83-4f53-adf7-c0a0c965ff17.jpg"),
("Setka kanot tovuq 1kg", 95000, "https://www.seriouseats.com/thmb/14Zpihnf3sr_0KvjIMeG86LyrWc=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/spicy-lamb-skewers-chinese-street-food-recipe-step-06-Collage-9c8c4dcbf8564abf9d211e1a9863d945.jpg"),
("Bagir shashlik", 18000, "https://i.ytimg.com/vi/vP9iuDDmwA0/maxresdefault.jpg"),
("Setka bagir 1kg", 180000, "https://i.ytimg.com/vi/Jnf8eghBwxI/maxresdefault.jpg"),
("Sirniy katlet 100gr", 25000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSo39Cm0bokuLR0idi1zEYg81X8ntjeOvyrXw&s"),
("Sirniy katlet katta", 85000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSo39Cm0bokuLR0idi1zEYg81X8ntjeOvyrXw&s"),
("barbekyu 1kg", 160000, "https://png.pngtree.com/png-clipart/20240323/original/pngtree-sausage-grill-food-png-image_14659194.png"),
("Qoy goshti 1kg steyk", 270000, "https://the-challenger.ru/wp-content/uploads/2016/02/Stejk-iz-baraniny.jpg"),
("Gijduvon shashlik 70gr", 14000, "https://i.ytimg.com/vi/aBC4gTWbBiU/maxresdefault.jpg"),
("Vaguri 1kg", 250000, "https://avatars.mds.yandex.net/get-altay/1090799/2a00000186b2247f1b68d4b78a0a4a538cde/L_height"),
("Xom ijjon 1kg", 150000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS6_TeOE5q38_6M7sFRT-d2Z3Mad9PoqNaU8A&s"),
("Krilishka shashliik 150gr", 15000, "https://www.restoran-shafran.uz/image/cache/catalog/product/shashliki/kurinie-krilishki-300x200.jpg"),
("Kfc", 95000, "https://www.yummytummyaarthi.com/wp-content/uploads/2023/08/kfc-chicken-1-500x500.jpeg"),
],
"xamir": [
("Gomma", 12000, "https://img-global.cpcdn.com/recipes/d1b6af0b6c1f9dcc/1200x630cq80/photo.jpg"),
("Qapshirma sirniy", 14000, "https://media.ovkuse.ru/images/recipes/09068489-c929-4e7f-a8e2-80de8b14089f/09068489-c929-4e7f-a8e2-80de8b14089f_420_420.webp"),
("Kotir barak", 55000, "https://dyj6gt4964deb.cloudfront.net/images/crop-e49cd18c-63e5-4b40-b7b3-5a0f3f49405f.jpeg"),
("Kadi barak", 55000, "https://i.ytimg.com/vi/azTvFu93WLg/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLAR0fhjQ-SfAAb1uRYSq-ankzWfNA"),
("Tuxuk barak", 12000, "https://upload.wikimedia.org/wikipedia/commons/3/3a/Tuxumbarak.jpg"),
("Kartoshka barak", 55000, "https://i.ytimg.com/vi/Y5TdGlMFbV8/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLAr_eaW9kIN6M9gkwkwxC3VTeseDA"),
("Barak asorti", 55000, "https://dyj6gt4964deb.cloudfront.net/images/dc36f168-f451-4a08-bb90-06e5f11282e1.jpeg"),
],    
"suyuq": [
("Osmo shorva 1 porsi", 40000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTetBPOSzJj2pLH0y-kSmtoVaQrFbGjahYVhw&s"),
("Osmo sho'rva 0.5", 25000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTetBPOSzJj2pLH0y-kSmtoVaQrFbGjahYVhw&s"),
("Mastava", 35000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTZ_oOvyZK4J0lOZvQ7d6GE71z2Ni8SKJkY2g&s"),
("Borsh", 40000, "https://s1.eda.ru/StaticContent/Photos/Upscaled/120131085552/171206075835/p_O.jpg"),
("Unoshu 1porsi", 30000, "https://i.ytimg.com/vi/MTnD7bLYD48/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLBa0-451GdUUcX5lEO3X3ho54JhjQ"),
("Unoshu 0.5L", 25000, "https://i.ytimg.com/vi/MTnD7bLYD48/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLBa0-451GdUUcX5lEO3X3ho54JhjQ"),
("Plimen shorva", 35000, "https://i.ytimg.com/vi/W7moXoRQ-1w/sddefault.jpg"),
("Tiftil sho'rva 1porsi", 35000, "https://pazanda.ucoz.com/_nw/2/82967593.jpg"),
],
"ichimlik": [
("Cola 1.5L", 17000, "https://images.uzum.uz/cia493tenntd8rfc2s40/original.jpg"),
("Fanta 1.5L", 17000, "https://www.torontopizza.com.cy/menu/menu/473-large_default/fanta-15l.jpg"),
("Pepsi 1.5L", 20000, "https://yukber.uz/image/cache/catalog/product/YK0363/YK0363-700x700.jpg"),
("Chortoq", 8000, "https://officemax.uz/_next/image?url=%2Fmedia%2Fuploads%2Fcl73bllennt861ip6f1g.jpg&w=1200&q=75"),
("Moxito", 12000, "https://ir.ozone.ru/s3/multimedia-1-q/c1000/7349572070.jpg"),
("Borjomi", 20000, "https://hinkali-tancevali.ru/wp-content/uploads/2023/05/%D0%91%D0%BE%D1%80%D0%B6%D0%BE%D0%BC%D0%B8-min-scaled.jpg"),
("Ayron", 11000, "https://cdn.delever.uz/delever/1a0bae1a-3399-4b88-a981-152ceb2b7dda"),
("Ayron 1l grafii", 16000, "https://cdn.delever.uz/delever/1a0bae1a-3399-4b88-a981-152ceb2b7dda"),
("Qatiq", 8000, "https://i.ytimg.com/vi/isGhFrryJjA/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLBkWqukUS82okXiFr9IpybOHCZLWA"),
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
("Sheyx tovuq broller", 85000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSw2rBvsObj7djpGB_HdUMQTzB5hX56UnCZ6g&s"),
("Sheyx qaymoqo kabob 1 porsi", 150000, "https://prostokvashino.ru/upload/resize_cache/iblock/f55/800_800_0/f5546bc7661a7c0937b9e486aaca6f2a.jpg"),
("Sheyx saryogo dil", 85000, "https://images.gastronom.ru/5uRdTeWfcDQpawZ1yqI8rOQU7Q6Hb4YDIluI7tj_XHc/pr:recipe-cover-image/g:ce/rs:auto:0:0:0/L2Ntcy9hbGwtaW1hZ2VzL2NlMWVlZWE2LTAxOWItNDZiOS05YmUzLWQzYWYyYjc1MDhjNC5qcGc.webp"),
("Sheyx koy mushak", 220000, "https://i.ytimg.com/vi/UZL0pGymtkg/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLAgvTCTnhh0qBZcmnH1LZeHm-lomg"),
("Sheyx setka kabob", 240000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcROlHAqooWJfWuLPuuY02j5LINbJVJL2LA8qg&s"),
("Sheyx setka kovurga", 240000, "https://whiskedawaykitchen.com/wp-content/uploads/2022/08/grilled-rack-of-lamb-7-scaled.jpg"),
("Sheyx sosiska barbekyu", 160000, "https://st4.depositphotos.com/3860131/27260/i/1600/depositphotos_272604724-stock-photo-grilled-sausage-addition-herbs-vegetables.jpg"),
("Sheyx setka bagir", 180000, "https://images.gastronom.ru/CmvzMKBB7WIQAbQm2CxHHMuqxozmIcRH6OrIESmcGsg/pr:recipe-cover-image/g:ce/rs:auto:0:0:0/L2Ntcy9hbGwtaW1hZ2VzLzZiZWVkYjg4LThlZDYtNDcwYS05NDAzLWMxODk5ZjQwOTg3Zi5KUEc.webp"),
("Sheyx kuskavoy mol 100gr", 24000, "https://www.afisha.uz/uploads/media/2015/10/0046463.jpg"),
],
"Salatlar":[
("Salonniy kizil pomidor", 10000, ""),
("Aprel", 40000, ""),
("sezar", 40000, ""),
("Grecheskiy", 50000, ""),
("Dollar", 45000, ""),
("Muroskoy kapriz", 45000, ""),
("Damskiy kapriz", 40000, ""),
("Gribnoy", 40000, ""),
("Gulshan", 240000, ""),
("Olivea", 30000, ""),
("Pomidor sous", 10000, ""),
("Fransuskiy salat", 35000, ""),
("Yaponiskiy", 40000, ""),
("Smak", 35000, ""),
("Karat", 40000, ""),
("turetskiy", 40000, ""),
("Achchiq chuchuk", 25000, ""),
("Svejiy", 25000, ""),
("Chakki", 5000, ""),
("Limon", 15300, ""),
("Salonniy asorti", 25000, ""),
("Ovoshshiy asorti", 40000, ""),
("Sous 1l", 30000, ""),
("Okrushka", 15000, ""),
("Kok pomidor 250gr", 7000, ""),
("Salonniy karam 250gr", 12000, ""),
("Salonniy bodring 250gr", 10000, ""),
("Ajji burch", 3000, ""),
("Zelen osorti", 10000, ""),
("norin", 25000, ""),
("Gashir chimchi", 10000, ""),
("Letniy Yaponiskiy", 25000, ""),
("Salat samira", 25000, ""),
("Uch kunlik 1kg", 45000, ""),
("Zveshniy domashniy", 20000, ""),
("Xurstyashki baqlajon", 35000, ""),
("Gulshan salat", 30000, ""),
("Svejiy bodring", 35000, ""),
("Kazi andalus", 75000, ""),
("Vitamin", 15000, ""),
("Typliy baqlajon", 40000, ""),
("Mojiza", 35000, ""),
("Gijduvon salat", 35000, ""),
("Ostri tayaksi", 45000, ""),
("Choban salat", 35000, ""),
("Chiroqchi salat", 18000, ""),
("Fetaksa 100gr", 25000, ""),
("Baqlajan rulet", 40000, ""),
],
"Xalodniy zakuska":[
("Myaskaya narezka bolshoy", 100000, "https://i.ytimg.com/vi/JlgAu6FtwDY/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLCvMCnrIgt4mGfM9cQTUpIFOQU9kg"),
("Dil xalodniy", 300000, "https://c8.alamy.com/comp/2D7EY8B/cold-appetizer-of-beef-tongue-with-fresh-salad-close-up-in-a-plate-on-the-table-horizontal-2D7EY8B.jpg"),
("Anjir", 25000, "https://www.mystore.in/s/62ea2c599d1398fa16dbae0a/65cb2a87e030e140c73f8bad/anjir-420x420.jpeg"),
("Qovun", 20000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTXWjsMrBSJtQyJo2Nf-w7bBewBxyA5C7KVhQ&s"),
("Fruqtuviy asorti", 150000, "https://shafran-kafe.ru/storage/2024/11/e661126398b5aeeb8e55259faf0c517a.jpg"),
("Tarvuz", 15000, "https://pbs.twimg.com/media/DjgnZDgXgAM318-.jpg:large"),
("Sirniy asorti", 60000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTlW4hPN-_fvAz633jGv0P8G9NOz_RXcUvKaw&s"),
("Uzum 1kg", 50000, "https://bazarstore.az/cdn/shop/files/b56d15bfdd4a82d898f51f150f126f0e.jpg?v=1753352244"),
("Qulubnnika 1kg", 65000, "https://dostavo4ka.uz/upload-file/2023/12/19/6346/e3b225c0-0513-48ff-917e-4b0b77e82417.jpg"),
("Gilos 1kg", 75000, "https://storage.kun.uz/source/7/-Shulpq5vZhm72QpeJuV75cr8kaWXBMF.jpg"),
("Fruqtuvoy asorti 2 idisha", 170000, "https://shafran-kafe.ru/storage/2024/11/e661126398b5aeeb8e55259faf0c517a.jpg"),
("Mandarin 1kg", 35000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTlW4hPN-_fvAz633jGv0P8G9NOz_RXcUvKaw&s"),
("Banan", 35000, "https://fazo.tv/wp-content/uploads/2023/04/07044.jpg"),
("Mayda mandarin", 50000, "https://dostavo4ka.uz/upload-file/2023/03/19/6317/777d4d1b-9a66-45fa-be0c-90f273eb68eb.jpg"),
("Kivi", 65000, "https://stat.uz/images/kivi_ichi_140222.jpg"),
("Apelsin", 35000, "https://kaufland.media.schwarz/is/image/schwarz/citrus-fruit-orange-detail-1?JGstbGVnYWN5LW9uc2l0ZS00JA=="),
("Olma", 35000, "https://zamin.uz/uploads/posts/2025-03/640336f4e4_olma-apple-yabloko.webp"),
("Ananas", 85000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTlW4hPN-_fvAz633jGv0P8G9NOz_RXcUvKaw&s"),
("Meva osorti kovunli", 90000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTlW4hPN-_fvAz633jGv0P8G9NOz_RXcUvKaw&s"),
("Meva osorti ananasli", 100000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTlW4hPN-_fvAz633jGv0P8G9NOz_RXcUvKaw&s"),
("Ananas", 50000, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQbzWGZnk98qZqe4ZJ9_e14uvh6MK7X3VXcvg&s"),
("Shaptoli 1kg", 40000, "https://static.xabar.uz/crop/1/8/720_460_95_1884834325.jpg"),
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
# @dp.message(CommandStart())
# async def start(message: types.Message, state: FSMContext):
#     await message.answer("Ismingizni kiriting:")
#     await state.set_state(Register.name)
@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("⛔️ Bot vaqtincha ish faoliyatida emas")

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

        text = f"{name}\n💰 {price} so'm"

        if img:  # 👉 agar rasm BOR bo‘lsa
            await callback.message.answer_photo(
                photo=img,
                caption=text,
                reply_markup=kb
            )
        else:  # 👉 agar rasm YO‘Q bo‘lsa
            await callback.message.answer(
                text,
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
