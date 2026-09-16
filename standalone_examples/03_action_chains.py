"""
03 — ActionChains: наведение мыши и управление ползунком с клавиатуры.

Нативное перетаскивание HTML5 рассмотрено отдельно в примере 04.
"""

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from _helpers import new_driver, show_element, site_url

# создаём драйвер
driver = new_driver()
# открываем страницу-полигон со сложными виджетами
driver.get(site_url("playground.html"))

# ---------- Наведение курсора (hover) ----------
# создаём локатор элемента, у которого есть CSS-подсказка при наведении
tooltip_locator = (By.CSS_SELECTOR, "[data-testid=tooltip-trigger]")
tooltip_trigger = driver.find_element(*tooltip_locator)
show_element(driver, tooltip_trigger)
# у WebElement нет метода "навести курсор" — это умеет только ActionChains
ActionChains(driver).move_to_element(tooltip_trigger).perform()
print("Tooltip text (from data-tooltip attribute):", tooltip_trigger.get_attribute("data-tooltip"))

# ---------- Управление ползунком клавиатурой ----------
slider_locator = (By.ID, "volume-slider")
slider = driver.find_element(*slider_locator)
show_element(driver, slider)
# кликаем по ползунку, чтобы поставить на него фокус, затем 10 раз жмём "вправо"
ActionChains(driver).click(slider).send_keys(Keys.ARROW_RIGHT * 10).perform()
value_label = driver.find_element(By.ID, "volume-value")
print("Slider value after 10x ARROW_RIGHT:", value_label.text)

# ---------- Удержание и отпускание кнопки мыши ----------
checkbox_locator = (By.ID, "enable-checkbox")
checkbox = driver.find_element(*checkbox_locator)
show_element(driver, checkbox)
# click_and_hold + release эмулируют "нажали и отпустили" отдельными шагами
ActionChains(driver).click_and_hold(checkbox).release(checkbox).perform()
toggle_btn = driver.find_element(By.ID, "toggle-target-btn")
print("Toggle button enabled after click_and_hold+release on checkbox:", toggle_btn.is_enabled())

# закрываем браузер
driver.quit()
