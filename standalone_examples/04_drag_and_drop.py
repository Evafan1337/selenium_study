"""
04 — Перетаскивание: почему одного ActionChains иногда недостаточно.

ActionChains отправляет синтетические события мыши. Некоторые браузеры не
преобразуют их в настоящие HTML5-события dragstart, dragover и drop, поэтому
для элементов draggable="true" может потребоваться JavaScript.

Скрипт сравнивает ActionChains и отправку событий DragEvent через JavaScript.
"""

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from _helpers import new_driver, show_element, site_url

# создаём драйвер
driver = new_driver()
driver.get(site_url("playground.html"))

# создаём локаторы для перетаскиваемого элемента и зоны сброса
draggable_locator = (By.ID, "draggable")
dropzone_locator = (By.ID, "dropzone")
# находим оба элемента на странице
draggable = driver.find_element(*draggable_locator)
dropzone = driver.find_element(*dropzone_locator)
# подсвечиваем оба, чтобы видеть, откуда и куда будем тащить
show_element(driver, draggable)
show_element(driver, dropzone)

print("Dropzone before:", dropzone.text)

# ---------- Способ 1: ActionChains.drag_and_drop ----------
ActionChains(driver).drag_and_drop(draggable, dropzone).perform()
print("Dropzone after ActionChains.drag_and_drop:", dropzone.text, "(often unchanged)")

# ---------- Способ 2: ручная отправка HTML5 drag-событий через JavaScript ----------
# это надёжная альтернатива, когда браузер игнорирует синтетические события мыши
driver.execute_script(
    """
    function fireEvent(name, element, dataTransfer) {
        const event = new Event(name, {bubbles: true, cancelable: true});
        event.dataTransfer = dataTransfer;
        element.dispatchEvent(event);
    }
    const dataTransfer = new DataTransfer();
    fireEvent('dragstart', arguments[0], dataTransfer);
    fireEvent('dragover', arguments[1], dataTransfer);
    fireEvent('drop', arguments[1], dataTransfer);
    """,
    draggable,
    dropzone,
)
print("Dropzone after JS-dispatched DragEvents:", dropzone.text, "(should say 'Dropped!')")

# закрываем браузер
driver.quit()
