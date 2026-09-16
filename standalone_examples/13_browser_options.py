"""
13 — Настройки браузера: headless-режим, размер окна и capabilities.

Chrome настраивается напрямую, чтобы показать параметры локального запуска и CI.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from _helpers import enable_demo, show_element

# ---------- Собираем настройки браузера до создания драйвера ----------
options = Options()
# Для CI раскомментируйте строку ниже. Для наглядной демонстрации она выключена.
# options.add_argument("--headless=new")
options.add_argument("--window-size=1280,900")
options.add_argument("--disable-gpu")        # Иногда требуется вместе с headless-режимом.
options.add_argument("--no-sandbox")         # Часто требуется внутри контейнеров.
options.add_argument("--mute-audio")
options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Скрываем сообщение об автоматизации.

# создаём драйвер с этими настройками — здесь не используется build_driver(),
# чтобы было видно "сырое" создание Chrome от начала и до конца
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
# добавляем подсветку и паузы к уже созданному драйверу
driver = enable_demo(driver)

# открываем крошечную страницу, собранную прямо в data:-адресе, без файла на диске
driver.get("data:text/html,<title>Browser options</title><h1>Visible Chrome demo</h1>")

# создаём локатор заголовка и подсвечиваем его
heading_locator = (By.TAG_NAME, "h1")
heading = driver.find_element(*heading_locator)
show_element(driver, heading)

print("Page title:", driver.title)
print("Window size:", driver.get_window_size())
print("Browser name/version:", driver.capabilities["browserName"], driver.capabilities["browserVersion"])

# закрываем браузер
driver.quit()
