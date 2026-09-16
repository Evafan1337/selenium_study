"""
11 — execute_script(): прямое чтение и изменение DOM и состояния страницы.
"""

import time

from selenium.webdriver.common.by import By

from _helpers import DEMO_DELAY, new_driver, show_element, site_url

# пауза между действиями, чтобы успеть увидеть результат JS-вызова на экране —
# execute_script() сам по себе ничего не подсвечивает и не ждёт
SLEEP = DEMO_DELAY

# создаём драйвер
driver = new_driver()
driver.get(site_url("catalog.html"))

# ---------- Читаем глобальную переменную JavaScript со страницы ----------
product_count = driver.execute_script("return PRODUCTS.length;")
print("PRODUCTS.length via JS:", product_count)

# ---------- Меняем значение ползунка напрямую через JS и "будим" слушателей ----------
# создаём локатор ползунка цены
slider_locator = (By.ID, "max-price")
slider = driver.find_element(*slider_locator)
show_element(driver, slider)
# просто присвоить .value недостаточно: страница слушает событие 'input',
# поэтому отправляем его вручную вторым шагом
driver.execute_script(
    """
    arguments[0].value = arguments[1];
    arguments[0].dispatchEvent(new Event('input', {bubbles: true}));
    """,
    slider,
    75,
)
result_count = driver.find_element(By.ID, "result-count")
show_element(driver, result_count)
print("Result count after JS-setting price slider to 75:", result_count.text)

# ---------- Прокручиваем страницу вниз перед взаимодействием ----------
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
print("Scrolled to bottom, scrollY =", driver.execute_script("return window.scrollY;"))
# пауза, чтобы увидеть сам скролл, а не только координату в консоли
time.sleep(SLEEP)

# ---------- Подсвечиваем элемент вручную, напрямую через JS ----------
# так работает helper show_element() под капотом — но здесь мы делаем это сами,
# без обёртки, чтобы увидеть код "изнутри"
card_locator = (By.CSS_SELECTOR, "[data-testid=product-card]")
card = driver.find_element(*card_locator)
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", card)
driver.execute_script("arguments[0].style.border = '3px solid red';", card)
print("Injected a red border via JS for visual debugging.")
# пауза перед закрытием — иначе красная рамка появится и тут же исчезнет вместе с браузером
time.sleep(SLEEP)

# закрываем браузер
driver.quit()
