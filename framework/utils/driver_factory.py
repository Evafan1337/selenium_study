"""
Создаёт настроенный экземпляр WebDriver. Код вынесен из conftest.py, чтобы
автономные примеры могли использовать его без зависимости от pytest.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from framework.utils import config


def build_driver(browser: str = None, headless: bool = None) -> webdriver.Remote:
    browser = (browser or config.BROWSER).lower()
    headless = config.HEADLESS if headless is None else headless

    if browser == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
    else:
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1400,1000")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    # Намеренно не вызываем driver.implicitly_wait(): весь BasePage построен
    # на явных WebDriverWait, а implicit wait, включённый одновременно с ними,
    # незаметно замедляет и путает ожидания (Selenium сам не рекомендует их
    # смешивать) — драйвер должен ждать ровно так, как попросит вызывающий код.
    return driver
