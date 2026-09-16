"""
06 — Iframe: элементы внутри фрейма недоступны Selenium до переключения
контекста, а после возврата снова становятся недоступны.
"""

import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from _helpers import DEMO_DELAY, new_driver, show_element, site_url

# пауза между действиями, чтобы успеть увидеть каждый шаг, а не просто
# прочитать итог в консоли
SLEEP = DEMO_DELAY

# создаём драйвер
driver = new_driver()
driver.get(site_url("playground.html"))

# ---------- Пытаемся найти элемент из iframe, не переключаясь внутрь ----------
# это специально демонстрационный try/except: исключение здесь — ожидаемый
# результат, а не ошибка, которую нужно "тушить"
try:
    driver.find_element(By.ID, "iframe-input")
    print("Found #iframe-input from the top-level document (unexpected!)")
except NoSuchElementException:
    print("As expected: #iframe-input is NOT visible from the top-level document")

# ---------- Переключаемся внутрь iframe ----------
# создаём локатор самого тега <iframe>
frame_locator = (By.ID, "content-frame")
frame_element = driver.find_element(*frame_locator)
# подсвечиваем сам iframe, прежде чем "войти" внутрь него
show_element(driver, frame_element)
driver.switch_to.frame(frame_element)
# сам переход внутрь iframe ничего не меняет на экране — пауза здесь просто
# даёт осознать момент переключения контекста, прежде чем читать элемент дальше
time.sleep(SLEEP)

# теперь мы внутри документа iframe — ищем и заполняем поле внутри него
iframe_input = driver.find_element(By.ID, "iframe-input")
iframe_input.send_keys("hello from the outside")
# пауза, чтобы увидеть введённый текст до того, как прочитаем эхо рядом
time.sleep(SLEEP)
iframe_echo = driver.find_element(By.ID, "iframe-echo")
show_element(driver, iframe_echo)
print("Echoed inside the frame:", iframe_echo.text)

# ---------- Возвращаемся в основной документ ----------
# пока мы не вызовем default_content(), driver "думает", что мы всё ещё внутри iframe
driver.switch_to.default_content()
brand = driver.find_element(By.CLASS_NAME, "brand")
show_element(driver, brand)
print("Back in the main document, brand text:", brand.text)

# закрываем браузер
driver.quit()
