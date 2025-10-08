import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

CATEGORY_FILE = "ke.json"
PRODUCT_FILE = "yandex_products.json"
CHROME_PATH = r'C:\Users\user\Desktop\bot\chromedriver.exe'


# ---------------- CATEGORIES SCRAPER ----------------
def get_yandex_categories(link):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(service=Service(CHROME_PATH) )
    all_categories = []

    try:
        driver.get(link)
        wait = WebDriverWait(driver, 15)
        # --- Проверка и закрытие модалки ---
        try:
            modal = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='dialog']"))
            )
            print("Модалка найдена. Закрываем...")
            close_btn = modal.find_element(By.CSS_SELECTOR, "button[data-auto='close-popup']")
            close_btn.click()
            print("Модалка закрыта.")
            time.sleep(1)
        except TimeoutException:
            print("Модалка не появилась — продолжаем дальше.")
        except NoSuchElementException:
            print("Кнопка закрытия не найдена — возможно, другая модалка.")
        catalog_btn = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-zone-name='catalog']"))
        )
        catalog_btn.click()
        time.sleep(2)

        categories = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href^='/catalog']"))
        )
        for category in categories:
            try:
                spans = category.find_elements(By.CSS_SELECTOR, "span._3W4t0")
                if spans:
                    title = spans[0].text.strip()
                else:
                    continue

                href = category.get_attribute("href")
                if title and href:
                    all_categories.append({"title": title, "url": href})
            except Exception as e:
                print("Ошибка при извлечении категории: ", e)

    finally:
        driver.quit()

    with open(CATEGORY_FILE, "w", encoding="utf-8") as f:
        json.dump(all_categories, f, ensure_ascii=False, indent=4)

    return all_categories


# ---------------- PRODUCTS SCRAPER ----------------
def get_yandex_products(category_link):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(service=Service(CHROME_PATH), options=options)
    all_products = []

    try:
        driver.get(category_link)
        wait = WebDriverWait(driver, 15)

        products_cards = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-id]'))
        )

        for card in products_cards:
            try:
                title = card.find_element(By.CSS_SELECTOR, '[data-zone-name="title"]').text
            except:
                title = "Нет названия"

            try:
                price_element = card.find_element(By.CSS_SELECTOR, '.ds-text_color_price-sale.ds-text_headline-5_bold')
                price = price_element.text.strip()
            except:
                price = "Нет цены"

            try:
                rating_block = card.find_element(By.CSS_SELECTOR, '[data-zone-name="rating"]')
                hidden_spans = rating_block.find_elements(By.CSS_SELECTOR, '.ds-visuallyHidden')

                if len(hidden_spans) >= 2:
                    rating_text = hidden_spans[0].text  # "Рейтинг товара: 4.9 из 5"
                    count_text = hidden_spans[1].text  # "на основе 49 оценок"

                    import re
                    rating_value = re.search(r"([\d.]+)", rating_text).group(1)
                    count_value = re.search(r"(\d+)", count_text).group(1)
                    rating = f"{rating_value} на основе {count_value} оценок"
                else:
                    rating = "Нет рейтинга"
            except:
                rating = "Нет рейтинга"

            try:
                link = card.find_element(By.CSS_SELECTOR, 'a').get_attribute("href")
            except:
                link = "Нет ссылки"

            all_products.append({
                "title": title,
                "price": price,
                "rating": rating,
                "url": link
            })



    finally:
        driver.quit()

    with open(PRODUCT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_products, f, ensure_ascii=False, indent=4)

    return all_products


# ---------------- TEST RUN ----------------
if __name__ == "__main__":
    print("📦 Получаем категории с Yandex Market...")
    cats = get_yandex_categories()
    print(f"Найдено категорий: {len(cats)}")

    # Для теста: получаем товары первой категории
    if cats:
        print(f"\n🛒 Загружаем товары из категории: {cats[0]['title']}")
        products = get_yandex_products(cats[0]["url"])
        print(f"Найдено товаров: {len(products)}")