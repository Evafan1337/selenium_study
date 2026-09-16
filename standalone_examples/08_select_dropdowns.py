"""
08 — Класс Select: одиночные и множественные выпадающие списки.

Select предоставляет понятные методы выбора по значению, тексту и индексу.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from _helpers import new_driver, show_element, site_url

# создаём драйвер
driver = new_driver()
driver.get(site_url("product.html?id=1"))

# ---------- Одиночный выбор ----------
# создаём локатор обычного <select> и находим по нему элемент
quantity_locator = (By.ID, "quantity-select")
quantity_element = driver.find_element(*quantity_locator)
show_element(driver, quantity_element)
# оборачиваем сырой WebElement в Select — так удобнее работать с <option>
quantity = Select(quantity_element)
print("Available quantities:", [o.text for o in quantity.options])
# выбираем опцию по атрибуту value
quantity.select_by_value("3")
print("Selected quantity:", quantity.first_selected_option.text)

# ---------- Множественный выбор ----------
driver.get(site_url("playground.html"))
languages_locator = (By.ID, "multi-select")
languages_element = driver.find_element(*languages_locator)
show_element(driver, languages_element)
languages = Select(languages_element)
print("Is multi-select multiple?", languages.is_multiple)

# выбираем сразу два варианта по видимому тексту опции
languages.select_by_visible_text("Python")
languages.select_by_visible_text("Go")
selected = [o.text for o in languages.all_selected_options]
print("Selected languages:", selected)

# снимаем выбор с одного из вариантов
languages.deselect_by_visible_text("Go")
print("After deselecting Go:", [o.text for o in languages.all_selected_options])

# закрываем браузер
driver.quit()
