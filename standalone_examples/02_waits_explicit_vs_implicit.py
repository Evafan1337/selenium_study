"""
02 — Сравнение отсутствия ожидания, implicit wait и explicit wait.

Кнопка показывает скрытый блок через две секунды. Пример объясняет, почему
наличия элемента в DOM недостаточно, когда важна его видимость.
"""

import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from _helpers import new_driver, show_element, site_url

# локаторы понадобятся во всех трёх попытках — создаём их один раз
LOAD_BTN = (By.ID, "load-btn")
LOADED_CONTENT = (By.ID, "loaded-content")

# ==================== Попытка 1: вообще без ожидания ====================
# элемент есть в DOM сразу после клика, но контент на странице появляется
# с задержкой в 2 секунды — без ожидания мы придём слишком рано

# создаём драйвер для первой попытки
driver = new_driver()
# явно отключаем implicit wait, чтобы find_element не ждал сам по себе
driver.implicitly_wait(0)
driver.get(site_url("playground.html"))
# ищем кнопку по локатору и кликаем по ней
driver.find_element(*LOAD_BTN).click()
# сразу же, без паузы, ищем элемент, который появляется с задержкой
element = driver.find_element(*LOADED_CONTENT)
print("Attempt 1 (no wait): present in DOM, displayed =", element.is_displayed())
# закрываем браузер первой попытки
driver.quit()

# ==================== Попытка 2: implicit wait ====================
# implicit wait заставляет find_element ждать, пока элемент появится в DOM,
# но не проверяет, что элемент виден — а в нашем случае он именно скрыт,
# а не отсутствует

driver = new_driver()
# ставим неявное ожидание короче задержки на странице (2 секунды)
driver.implicitly_wait(1)
driver.get(site_url("playground.html"))
driver.find_element(*LOAD_BTN).click()
element = driver.find_element(*LOADED_CONTENT)
print("Attempt 2 (1s implicit wait): returned immediately, displayed =", element.is_displayed())
driver.quit()

# ==================== Попытка 3: explicit wait ====================
# WebDriverWait с expected_conditions ждёт именно нужного состояния —
# в данном случае видимости элемента, а не просто его присутствия в DOM

driver = new_driver()
driver.get(site_url("playground.html"))
driver.find_element(*LOAD_BTN).click()
# создаём объект явного ожидания с таймаутом в 5 секунд
wait = WebDriverWait(driver, 5)
start = time.time()
try:
    # ждём именно видимости элемента, а не просто его наличия в DOM
    element = wait.until(EC.visibility_of_element_located(LOADED_CONTENT))
    # подсвечиваем элемент, который дождались явным ожиданием
    show_element(driver, element)
    print(f"Attempt 3 (explicit wait): found '{element.text}' after {time.time() - start:.2f}s")
except TimeoutException:
    print("Attempt 3 (explicit wait): unexpectedly timed out")

# закрываем браузер третьей попытки
driver.quit()
