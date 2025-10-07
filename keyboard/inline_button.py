from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from pathlib import Path
import hashlib
import json

CATEGORIES_PATH = Path(__file__).parent.parent / "scrapers" / "categories.json"

def load_uzum_categories():
    try:
        with open(CATEGORIES_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def start_keyboard():
    kb = InlineKeyboardBuilder()
    kb.row(
        InlineKeyboardButton(text="🚀 Начать", callback_data="start_bot")
    )
    return kb.as_markup()

def marketplace_keyboard():
    kb = InlineKeyboardBuilder()
    kb.row(
        InlineKeyboardButton(text="🍇 Uzum", callback_data="market_uzum"),
        InlineKeyboardButton(text="🟨 Yandex", callback_data="market_yandex")
    )
    kb.row(InlineKeyboardButton(text='📞 Поддержка', callback_data="support"))
    return kb.as_markup()

CATEGORIES_PAGE_SIZE = 6
PRODUCTS_PAGE_SIZE = 6

def uzum_categories_keyboard(categories, page: int = 0):
    total = len(categories)
    start = page * CATEGORIES_PAGE_SIZE
    end = start + CATEGORIES_PAGE_SIZE
    current_page_items = categories[start:end]

    kb = InlineKeyboardBuilder()

    for c in current_page_items:
        text = c["title"]
        callback_data = f"uzum_{hashlib.md5(text.encode()).hexdigest()[:8]}"
        kb.row(InlineKeyboardButton(text=text, callback_data=callback_data))

    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(text="⬅️", callback_data=f"uzum_page_{page - 1}"))
    if end < total:
        nav_buttons.append(InlineKeyboardButton(text="➡️", callback_data=f"uzum_page_{page + 1}"))

    if nav_buttons:
        kb.row(*nav_buttons)

    kb.row(InlineKeyboardButton(text="🔙 Назад", callback_data="start_bot"))

    return kb.as_markup()

def uzum_products_keyboard(products, page=0):
    kb = InlineKeyboardBuilder()
    total = len(products)
    start = page * PRODUCTS_PAGE_SIZE
    end = start + PRODUCTS_PAGE_SIZE
    current_products = products[start:end]

    for i, p in enumerate(current_products, start=start):
        kb.row(InlineKeyboardButton(
            text=p['title'],
            callback_data=f"product_{i}"  # индекс вместо хэша
        ))

    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(text="⬅️", callback_data=f"products_page_{page - 1}"))
    if end < total:
        nav_buttons.append(InlineKeyboardButton(text="➡️", callback_data=f"products_page_{page + 1}"))

    if nav_buttons:
        kb.row(*nav_buttons)

    # Back to category
    kb.row(InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_categories"))

    return kb.as_markup()

def product_details_keyboard(product):
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="🔗 Перейти по ссылке", url=product['url']))
    kb.row(InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_products"))

    return kb.as_markup()

# === ПАРАМЕТРЫ ===
YANDEX_CATEGORIES_PAGE_SIZE = 6
YANDEX_PRODUCTS_PAGE_SIZE = 6


# === КАТЕГОРИИ ===
def yandex_categories_keyboard(categories, page: int = 0):
    total = len(categories)
    start = page * YANDEX_CATEGORIES_PAGE_SIZE
    end = start + YANDEX_CATEGORIES_PAGE_SIZE
    current_page_items = categories[start:end]

    kb = InlineKeyboardBuilder()

    for c in current_page_items:
        text = c["title"]
        callback_data = f"yandex_{hashlib.md5(text.encode()).hexdigest()[:8]}"
        kb.row(InlineKeyboardButton(text=text, callback_data=callback_data))

    # Навигация между страницами
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(text="⬅️", callback_data=f"yandex_page_{page - 1}"))
    if end < total:
        nav_buttons.append(InlineKeyboardButton(text="➡️", callback_data=f"yandex_page_{page + 1}"))

    if nav_buttons:
        kb.row(*nav_buttons)

    # Кнопка "Назад"
    kb.row(InlineKeyboardButton(text="🔙 Назад", callback_data="start_bot"))

    return kb.as_markup()


# === ПРОДУКТЫ ===
def yandex_products_keyboard(products, page=0):
    kb = InlineKeyboardBuilder()
    total = len(products)
    start = page * YANDEX_PRODUCTS_PAGE_SIZE
    end = start + YANDEX_PRODUCTS_PAGE_SIZE
    current_products = products[start:end]

    for i, p in enumerate(current_products, start=start):
        kb.row(InlineKeyboardButton(
            text=p['title'],
            callback_data=f"yandex_product_{i}"
        ))

    # Навигация по страницам
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(text="⬅️", callback_data=f"yandex_products_page_{page - 1}"))
    if end < total:
        nav_buttons.append(InlineKeyboardButton(text="➡️", callback_data=f"yandex_products_page_{page + 1}"))

    if nav_buttons:
        kb.row(*nav_buttons)

    # Назад к категориям
    kb.row(InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_yandex_categories"))

    return kb.as_markup()


# === ДЕТАЛИ ПРОДУКТА ===
def yandex_product_details_keyboard(product):
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text="🔗 Перейти по ссылке", url=product['url']))
    kb.row(InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_yandex_products"))
    return kb.as_markup()





