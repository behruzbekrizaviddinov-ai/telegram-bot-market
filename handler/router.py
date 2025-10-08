from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from keyboard import *
from selenium.common.exceptions import TimeoutException
from scraper import *   # здесь уже должны быть get_uzum_... и get_yandex_...
import hashlib

router = Router()

@router.message(CommandStart())
async def program_start(message: types.Message):
    user = message.from_user.first_name
    hello_text = (
        f"👋 Привет, *{user}!* \n\n"
        "**MindBuy** 🛍️ — место, где товары говорят сами за себя!\n\n"
        "Здесь можно:\n"
        "📂 Просматривайте товары по категориям\n"
        "💰 Сравнивайте и сортируйте товары\n"
        "⭐ Проверяйте рейтинги и отзывы\n"
        "🔔 Получайте уведомления о лучших предложениях!\n\n"
    )
    await message.answer(hello_text, parse_mode="Markdown", reply_markup=marketplace_keyboard())


@router.callback_query(lambda c: c.data == "start_bot")
async def start_button(callback: types.CallbackQuery):
    if callback.message:
        await callback.message.delete()

    user = callback.from_user.first_name
    hello_text = (
        f"👋 Привет, *{user}!* \n\n"
        "**MindBuy** 🛍️ — место, где товары говорят сами за себя!\n\n"
        "Здесь можно:\n"
        "📂 Просматривайте товары по категориям\n"
        "💰 Сравнивайте и сортируйте товары\n"
        "⭐ Проверяйте рейтинги и отзывы\n"
        "🔔 Получайте уведомления о лучших предложениях!\n\n"
    )
    await callback.message.answer(hello_text, parse_mode="Markdown", reply_markup=marketplace_keyboard())
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("support"))
async def help_command(callback: types.CallbackQuery):
    help_text = (
        "🛠 *MindBuy — Поддержка*\n\n"
        "Привет! Вот как пользоваться ботом:\n\n"
        "1️⃣ *Выберите маркетплейс*\n"
        "   - Нажмите кнопку *Uzum* или *Yandex Market*, чтобы выбрать, где искать товары.\n\n"
        "2️⃣ *Категории*\n"
        "   - После выбора маркетплейса появятся кнопки категорий.\n\n"
        "3️⃣ *Подкатегории и фильтры*\n"
        "   - В подкатегориях можно выбрать товары и смотреть фильтры ⭐💎\n\n"
        "4️⃣ *Команды*\n"
        "   /start — запустить бота заново\n\n"

        "💡 Совет: используйте кнопки под сообщениями — это быстрее и удобнее! 🚀"
    )

    await callback.message.answer(help_text, parse_mode="Markdown", reply_markup=start_keyboard())
    await callback.answer()


PAGE_SIZE = 6
PRODUCTS_PAGE_SIZE = 6

categories_cache = {}
products_cache = {}

# ---------------------------------------------------------------------
# ----------------------------- UZUM ---------------------------------
# ---------------------------------------------------------------------

@router.message(Command("uzum"))
async def market_uzum(message: types.Message):
    chat_id = message.chat.id
    loading_msg = await message.answer("Поиск категории... ⏳")

    try:
        categories = get_uzum_categories("https://uzum.uz/ru")
        categories_cache[chat_id] = categories
        await loading_msg.delete()
    except TimeoutException:
        await loading_msg.delete()
        await message.answer("Не удалось загрузить категории 😢 Попробуйте позже.")
        return

    text = (
        "🛍 Добро пожаловать в 🍇 **Uzum Market**!\n\n"
        "Выберите категорию, чтобы начать поиск товаров. ⬇️\n\n"
        "💡 Подсказка: используйте кнопки для навигации — это быстрее и удобнее!"
    )

    await message.answer(
        text,
        reply_markup=uzum_categories_keyboard(categories, page=0),
        parse_mode="Markdown"
    )


@router.callback_query(lambda c: c.data.startswith("uzum_page_"))
async def uzum_categories_pagination(callback: types.CallbackQuery):
    await callback.answer()
    chat_id = callback.message.chat.id
    page = int(callback.data.split("_")[-1])

    categories = categories_cache.get(chat_id)
    if not categories:
        await callback.message.edit_text(
            "Категории пока не загружены 😢\nНажмите /uzum чтобы обновить."
        )
        return

    await callback.message.edit_text(
        "🛍 Выберите категорию ⬇️",
        parse_mode="Markdown",
        reply_markup=uzum_categories_keyboard(categories, page)
    )


@router.callback_query(lambda c: c.data.startswith("uzum_"))
async def uzum_category_callback(callback: types.CallbackQuery):
    await callback.answer()
    chat_id = callback.message.chat.id

    category_hash = callback.data.split("_")[1]
    categories = categories_cache.get(chat_id, [])
    category = next(
        (c for c in categories if hashlib.md5(c["title"].encode()).hexdigest()[:8] == category_hash),
        None
    )

    if not category:
        await callback.message.answer("❌ Не удалось найти категорию.")
        return

    loading_msg = await callback.message.answer(f"⏳ Загружаем товары категории {category['title']}...")
    products = get_uzum_products(category["url"])
    await loading_msg.delete()

    if not products:
        await callback.message.answer("Пока нет товаров в этой категории 😢")
        return

    products_cache[chat_id] = products

    await callback.message.edit_text(
        f"🛒 Товары категории **{category['title']}**\\. Выберите товар ⬇️",
        parse_mode="Markdown",
        reply_markup=uzum_products_keyboard(products, page=0)
    )


@router.callback_query(lambda c: c.data.startswith("products_page_"))
async def uzum_products_pagination(callback: types.CallbackQuery):
    await callback.answer()
    chat_id = callback.message.chat.id
    page = int(callback.data.split("_")[-1])

    products = products_cache.get(chat_id)
    if not products:
        await callback.message.answer("Товары пока не загружены 😢")
        return

    text = "🛒 Товары категории:\n\n"

    await callback.message.edit_text(
        text,
        parse_mode="Markdown",
        reply_markup=uzum_products_keyboard(products, page)
    )


@router.callback_query(lambda c: c.data.startswith("back_to_categories"))
async def back_to_categories(callback: types.CallbackQuery):
    if callback.message:
        await callback.message.delete()
    await callback.answer()
    await market_uzum(callback.message)


@router.callback_query(lambda c: c.data.startswith("product_"))
async def product_detail_callback(callback: types.CallbackQuery):
    await callback.answer()
    chat_id = callback.message.chat.id
    products = products_cache.get(chat_id)
    if not products:
        await callback.message.answer("Товары пока не загружены 😢")
        return

    index = int(callback.data.split("_")[-1])
    if index >= len(products):
        await callback.message.answer("Товар не найден 😢")
        return

    product = products[index]
    text = (
        f"✨🛍 **{product['title']}** ✨\n\n"
        f"💰 Цена: **{product['price']} сум**\n"
        f"📅 Рассрочка: *{product['price_per_month']}* в месяц\n"
        f"🔗 [Открыть в Uzum]({product['url']})"
    )

    await callback.message.answer(text, parse_mode="Markdown", reply_markup=product_details_keyboard(product))


@router.callback_query(lambda c: c.data.startswith("back_to_products"))
async def back_to_products(callback: types.CallbackQuery):
    if callback.message:
        await callback.message.delete()
    await callback.answer()


# ---------------------------------------------------------------------
# -------------------------- YANDEX MARKET ----------------------------
# ---------------------------------------------------------------------

@router.message(Command("yandex"))
async def market_yandex(message: types.Message):
    chat_id = message.chat.id
    loading_msg = await message.answer("🔎 Загружаем категории Yandex Market...")

    try:
        categories = get_yandex_categories("https://market.yandex.uz/")
        categories_cache[chat_id] = categories
        await loading_msg.delete()
    except TimeoutException:
        await loading_msg.delete()
        await message.answer("Не удалось загрузить категории 😢 Попробуйте позже.")
        return

    text = (
        "🛍 Добро пожаловать в 💛 **Yandex Market Uzbekistan**!\n\n"
        "Выберите категорию, чтобы начать поиск товаров. ⬇️"
    )

    await message.answer(
        text,
        reply_markup=yandex_categories_keyboard(categories, page=0),
        parse_mode="Markdown"
    )


@router.callback_query(lambda c: c.data.startswith("yandex_page_"))
async def yandex_categories_pagination(callback: types.CallbackQuery):
    await callback.answer()
    chat_id = callback.message.chat.id
    page = int(callback.data.split("_")[-1])

    categories = categories_cache.get(chat_id)
    if not categories:
        await callback.message.edit_text("Категории пока не загружены 😢\nНажмите /yandex чтобы обновить.")
        return

    await callback.message.edit_text(
        "🛍 Выберите категорию ⬇️",
        parse_mode="Markdown",
        reply_markup=yandex_categories_keyboard(categories, page)
    )


@router.callback_query(lambda c: c.data.startswith("yandex_") and not c.data.startswith(("yandex_product_", "yandex_products_page_")) )
async def yandex_category_callback(callback: types.CallbackQuery):
    await callback.answer()
    chat_id = callback.message.chat.id

    category_hash = callback.data.split("_")[-1]
    categories = categories_cache.get(chat_id, [])
    category = next(
        (c for c in categories if hashlib.md5(c["title"].encode()).hexdigest()[:8] == category_hash),
        None
    )

    if not category:
        await callback.message.answer("❌ Не удалось найти категорию.")
        return

    loading_msg = await callback.message.answer(f"⏳ Загружаем товары категории {category['title']}...")
    products = get_yandex_products(category["url"])
    await loading_msg.delete()

    if not products:
        await callback.message.answer("Пока нет товаров в этой категории 😢")
        return

    products_cache[chat_id] = products

    await callback.message.edit_text(
        f"🛒 Товары категории **{category['title']}**. Выберите товар ⬇️",
        parse_mode="Markdown",
        reply_markup=yandex_products_keyboard(products, page=0)
    )


@router.callback_query(lambda c: c.data.startswith("yandex_products_page_"))
async def yandex_products_pagination(callback: types.CallbackQuery):
    await callback.answer()
    chat_id = callback.message.chat.id
    page = int(callback.data.split("_")[-1])

    products = products_cache.get(chat_id)
    if not products:
        await callback.message.answer("Товары пока не загружены 😢")
        return

    text = "🛒 Товары категории:\n\n"

    await callback.message.edit_text(
        text,
        parse_mode="Markdown",
        reply_markup=yandex_products_keyboard(products, page)
    )


@router.callback_query(lambda c: c.data.startswith("yandex_product_"))
async def yandex_product_detail(callback: types.CallbackQuery):
    await callback.answer()
    chat_id = callback.message.chat.id
    products = products_cache.get(chat_id)
    if not products:
        await callback.message.answer("Товары пока не загружены 😢")
        return

    index = int(callback.data.split("_")[-1])
    if index >= len(products):
        await callback.message.answer("Товар не найден 😢")
        return

    product = products[index]
    text = (
        f"🛍 **{product['title']}**\n\n"
        f"💰 Цена: **{product['price']}**\n"
        f"🔗 [Открыть в Yandex Market]({product['url']})"
    )

    await callback.message.answer(text, parse_mode="Markdown", reply_markup=yandex_product_details_keyboard(product))


# ---------------------------------------------------------------------
# ----------------------------- Общие ---------------------------------
# ---------------------------------------------------------------------

@router.callback_query(lambda c: c.data.startswith("market_"))
async def callback_market(callback: types.CallbackQuery):
    await callback.answer()
    if callback.message:
        await callback.message.delete()

    if callback.data == "market_uzum":
        await market_uzum(callback.message)
    elif callback.data == "market_yandex":
        await market_yandex(callback.message)


@router.callback_query(lambda c: c.data == "back_home")
async def callback_back_home(callback: types.CallbackQuery):
    await callback.answer()
    await program_start(callback.message)