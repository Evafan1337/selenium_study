"""
07 — Несколько окон и вкладок: window_handles и switch_to.window().

Ссылка target="_blank" открывает вкладку, но драйвер остаётся в исходной,
пока мы явно не переключим контекст.
"""

import time

from selenium.webdriver.common.by import By

from _helpers import DEMO_DELAY, new_driver, site_url

# пауза между действиями — переключение вкладок в браузере происходит
# мгновенно, без паузы вы просто не успеете заметить, что вкладок стало две
SLEEP = DEMO_DELAY

# создаём драйвер
driver = new_driver()
driver.get(site_url("playground.html"))

# запоминаем набор хендлов (идентификаторов вкладок), которые открыты сейчас
original_handles = set(driver.window_handles)
print("Handles before click:", len(original_handles))

# создаём локатор ссылки, которая откроет новую вкладку (target="_blank")
new_tab_link_locator = (By.ID, "new-tab-link")
driver.find_element(*new_tab_link_locator).click()
# пауза, чтобы увидеть в браузере, что открылась вторая вкладка
time.sleep(SLEEP)

# у Selenium нет события "открылась новая вкладка" — сравниваем хендлы до и после
new_handle = (set(driver.window_handles) - original_handles).pop()
print("A new handle appeared:", new_handle != list(original_handles)[0])

# до явного переключения драйвер всё ещё "смотрит" в старую вкладку
print("Title before switching:", driver.title)

# переключаем фокус драйвера на новую вкладку
driver.switch_to.window(new_handle)
print("Title after switching:", driver.title)
print("URL after switching:", driver.current_url)
# пауза, чтобы увидеть содержимое именно новой вкладки, прежде чем её закроем
time.sleep(SLEEP)

# закрываем только новую вкладку — исходная остаётся открытой
driver.close()
# возвращаем фокус драйвера на исходную вкладку
driver.switch_to.window(list(original_handles)[0])
print("Back on the original tab, title:", driver.title)

# закрываем браузер (все оставшиеся вкладки) целиком
driver.quit()
