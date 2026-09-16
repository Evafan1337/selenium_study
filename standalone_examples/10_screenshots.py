"""
10 — Скриншоты всей страницы и отдельного элемента.
"""

from pathlib import Path

from selenium.webdriver.common.by import By

from _helpers import new_driver, show_element, site_url

# заранее готовим папку, куда будем сохранять скриншоты
OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# создаём драйвер
driver = new_driver()
driver.get(site_url("index.html"))

# ---------- Скриншот всей страницы целиком ----------
full_page_path = OUTPUT_DIR / "full_page.png"
driver.save_screenshot(str(full_page_path))
print("Saved full-page screenshot to", full_page_path)

# ---------- Скриншот одного элемента ----------
# создаём локатор карточки товара и находим первую на странице
card_locator = (By.CSS_SELECTOR, "[data-testid=product-card]")
first_card = driver.find_element(*card_locator)
show_element(driver, first_card)
element_path = OUTPUT_DIR / "first_product_card.png"
# screenshot() у самого WebElement снимает только этот элемент, а не всю страницу
first_card.screenshot(str(element_path))
print("Saved element-only screenshot to", element_path)

# ---------- Скриншот в виде base64-строки ----------
# удобно для встраивания прямо в HTML- или Allure-отчёт, без отдельного файла
b64 = driver.get_screenshot_as_base64()
print("Base64 screenshot length:", len(b64), "characters")

# закрываем браузер
driver.quit()
