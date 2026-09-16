# Учебный проект Selenium & Pytest — «ShopEasy»

Самодостаточный учебный репозиторий для изучения **Selenium WebDriver** и
**Pytest** на реалистичном, бизнес-ориентированном примере: небольшой
интернет-магазин (каталог, корзина, оформление заказа, личный кабинет,
регистрация) плюс отдельная страница-«полигон» со сложными UI-виджетами
(алерты, iframe, drag&drop, динамическая подгрузка, загрузка файлов,
мультиселект и т.д.).

Для запуска не нужен ни бэкенд, ни база данных, ни интернет — сайт
статический (HTML/CSS/JS), а «данные» хранятся в `localStorage`.

## Структура репозитория

```
site/                   Статический демо-магазин (можно открыть прямо в браузере,
                         либо тесты сами поднимут для него сервер)
  README.md             Карта сайта + заметки о локаторах для каждой страницы
  *.html, assets/...

framework/              Page Object Model фреймворк
  pages/                По одному классу на страницу: LoginPage, CartPage, CheckoutPage...
  utils/                driver_factory, локальный HTTP-сервер, конфиг

standalone_examples/    13 независимых скриптов, по одной фиче Selenium в каждом
  README.md             Что демонстрирует каждый скрипт и как его запустить

tests/                  Pytest-набор поверх Page Object'ов
  conftest.py           Фикстуры: браузер, локальный сервер, Page Object'ы, скриншот при падении
  test_*.py             47 тестов по 9 функциональным областям

test_styles/            Один и тот же сценарий логина в 4 уровнях абстракции
  README.md             driver/Page Object × без фикстур/с фикстурами — что каждая идея решает
                         Отдельная площадка: testpaths в pytest.ini её не подхватывает

requirements.txt
pytest.ini
```

## Быстрый старт

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Понадобится установленный Chrome (или Firefox, см. ниже); `webdriver-manager`
сам скачает подходящий драйвер при первом запуске.

### Запуск pytest-набора

```bash
pytest                                    # headless Chrome, все 47 тестов
pytest -m smoke                           # только тесты с меткой smoke
pytest tests/test_checkout.py -v          # один модуль
pytest tests/test_login.py::TestLogin::test_successful_login  # один конкретный тест
HEADLESS=false pytest tests/test_cart.py  # смотреть на браузер вживую
BROWSER=firefox pytest                    # запустить в Firefox
```

#### Выбор тестов

Маркеры, ключевые слова и точный путь до теста комбинируются:

```bash
pytest -m "smoke or regression"           # объединение маркеров
pytest -m "cart and not regression"       # маркер с исключением
pytest -k "login and not error"           # выбор по подстроке в имени теста
pytest tests/ -k "checkout"               # то же самое, но только внутри одной папки
pytest --collect-only -m checkout         # что будет выбрано — без запуска браузера
```

Маркеры объявлены в `pytest.ini`: `smoke`, `regression`, `login`,
`registration`, `catalog`, `product`, `cart`, `checkout`, `dashboard`,
`playground`. `addopts = --strict-markers` не даёт опечататься в имени —
незарегистрированный маркер сразу же валит сбор тестов ошибкой, а не тихо
пропускает тест мимо фильтра.

#### Переменные окружения

Поведение прогона настраивается окружением, без правки кода
(см. `framework/utils/config.py`):

| Переменная | По умолчанию | Что делает |
|---|---|---|
| `HEADLESS` | `true` | `false` — открыть настоящее окно браузера |
| `BROWSER` | `chrome` | `firefox` — запустить в Firefox вместо Chrome |
| `EXPLICIT_WAIT` | `10` | таймаут (сек) для всех `WebDriverWait` внутри `BasePage` |
| `ACTION_DELAY` | `0` | пауза (сек, можно дробная) после каждого действия Page Object — для наглядной демонстрации |

```bash
HEADLESS=false ACTION_DELAY=1 pytest -m smoke -v       # медленно и наглядно
BROWSER=firefox EXPLICIT_WAIT=15 pytest tests/test_checkout.py
```

Осознанно нет переменной для implicit wait: весь `framework/` построен на
явных ожиданиях, а смешивать implicit и explicit — задокументированный
антипаттерн Selenium (см. `standalone_examples/02_waits_explicit_vs_implicit.py`).

#### Повторные и частичные прогоны

```bash
pytest --lf          # только тесты, упавшие в прошлый раз (last-failed)
pytest --ff           # сначала упавшие в прошлый раз, потом остальные
pytest -x             # остановиться на первом же падении
pytest --maxfail=3    # остановиться после 3 падений
```

`addopts = -ra` в `pytest.ini` уже включён по умолчанию — в конце вывода
всегда есть сводка причин по каждому skip/xfail/error, даже без `-v`.

### Запуск отдельного standalone-примера

```bash
python standalone_examples/06_iframes.py
```

Полный список — в `standalone_examples/README.md`: это короткие
самостоятельные «уроки», не зависящие от pytest.

### Запуск учебной площадки test_styles

```bash
pytest test_styles/ -v                                     # все 4 уровня подряд
pytest test_styles/test_02_raw_driver_with_fixtures.py -v  # один конкретный уровень
```

Один и тот же сценарий логина, написанный 4 раза — с фикстурами и без,
с Page Object и без. Подробное сравнение — в `test_styles/README.md`.

### Просмотр сайта вручную

```bash
python -m http.server 8000 --directory site
# затем открыть http://localhost:8000
```

## Модульность: как pytest решает, что запускать

Весь выбор и импорт тестов управляется четырьмя строчками в `pytest.ini`:

```ini
pythonpath = .
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

Отсюда несколько не всегда очевидных следствий:

- **`testpaths = tests`** — голый `pytest` без аргументов ищет тесты только
  внутри `tests/`. Поэтому `test_styles/` не путается под ногами при обычном
  прогоне и не мешает CI: она не находится «случайно», путь к ней нужно
  указать явно (`pytest test_styles/`) — хотя её файлы и называются
  `test_*.py`, и формально подошли бы под `python_files`.
- **`python_files = test_*.py`** — файл обязан начинаться с `test_`, чтобы
  pytest вообще счёл его тестовым модулем. Именно поэтому скрипты в
  `standalone_examples/` (`01_locators.py`, `06_iframes.py`...) никогда не
  будут собраны pytest'ом, даже если явно указать путь к ним — они задуманы
  как самостоятельные программы (`python standalone_examples/06_iframes.py`),
  а не как тесты, и называются по номеру темы, а не с приставки `test_`.
- **`pythonpath = .`** — добавляет корень репозитория в `sys.path`, поэтому
  `from framework.pages.login_page import LoginPage` работает в `tests/` и
  `test_styles/` без единого `sys.path.insert`. `standalone_examples/`
  запускаются не через pytest, а напрямую (`python script.py`), поэтому у
  них тот же трюк сделан вручную — см. `sys.path.insert(...)` в `_helpers.py`.

Папки не знают друг о друге больше, чем нужно — зависимости идут в одну сторону:

```
site/                   не знает вообще ничего про Selenium/pytest — просто HTML/CSS/JS
framework/              знает про Selenium, ничего не знает про pytest
tests/                  знает про framework/ и про pytest (conftest.py, маркеры, Allure)
test_styles/            знает про framework/ и про pytest,
                        НЕ знает про tests/conftest.py — каждый файл объявляет
                        свои fixtures сам (см. test_styles/README.md)
standalone_examples/    знает про framework/utils/*, НЕ знает про pytest вообще
```

Именно поэтому `framework/` можно одинаково свободно использовать и в
pytest-наборе, и в одиночном скрипте, и в учебном файле без единого
fixture — он сам не тянет pytest как зависимость.

## Параметризация

`@pytest.mark.parametrize` запускает один и тот же тест несколько раз с
разными входными данными, без копирования его тела. В проекте пока нет ни
одного параметризованного теста, а готовый повод есть прямо сейчас:
`tests/test_product_page.py` проверяет `open_by_id()` на одном товаре за раз
(`open_by_id(1)`, `open_by_id(2)`, `open_by_id(3)` в разных тестах), хотя в
каталоге 6 товаров.

Как это выглядело бы:

```python
import pytest

@pytest.mark.parametrize("product_id", [1, 2, 3, 4, 5, 6])
def test_add_to_cart_updates_badge(self, product_page, product_id):
    product_page.open_by_id(product_id)
    product_page.add_to_cart()
    assert product_page.is_added_message_visible()
    assert product_page.cart_badge_count() == 1
```

pytest сам создаст 6 отдельных тестов — `test_add_to_cart_updates_badge[1]`
… `[6]` — каждый со своим id прямо в имени. Это удобно и для точечного
перезапуска (`pytest -k "test_add_to_cart_updates_badge and 4"`), и для
отчёта: упавший параметр виден по имени теста, не нужно раскапывать assert.

Несколько нюансов:
- **Несколько `@parametrize` подряд перемножаются** — два декоратора с 3 и 2
  значениями дадут 6 прогонов теста, по всем комбинациям.
- **`ids=`** — вместо `[1]`, `[2]`... в имени можно задать читаемые подписи:
  `@pytest.mark.parametrize("product_id", [1, 2], ids=["laptop", "mouse"])`.
- **Параметризовать можно и фикстуру, не только тест** —
  `@pytest.fixture(params=[...])`: тогда размножатся по всем значениям
  `params` все тесты, которые эту фикстуру используют, даже не упоминая
  параметризацию у себя в теле.
- `--strict-markers` из `pytest.ini` относится к меткам вида
  `@pytest.mark.smoke`, а не к `@pytest.mark.parametrize` — сам parametrize
  не требует регистрации в `markers =`, это встроенный механизм pytest, а
  не пользовательская метка.

Довести это до конца в `test_product_page.py` — открытая практика, см. раздел
«Как развивать проект дальше» ниже и этап 08 в roadmap-е.

## Отчёты Allure (опционально)

Allure уже подключён к тестам через `@allure.epic/@feature/@title`
и `@allure.step`, `allure-pytest` есть в `requirements.txt`. Использование
опционально — обычный `pytest` работает без него, а подключение Allure
занимает два дополнительных шага:

```bash
pip install allure-pytest          # уже есть в requirements.txt
pytest --alluredir=allure-results  # собрать результаты вместо обычного вывода (или вместе с ним)

# далее, если установлена Allure commandline (https://allurereport.org/docs/install/):
allure serve allure-results        # открывает интерактивный HTML-отчёт
# либо сгенерировать статическую папку с отчётом:
allure generate allure-results -o allure-report --clean
```

При падении теста скриншот автоматически прикладывается к отчёту Allure
(см. `pytest_runtest_makereport` в `tests/conftest.py`); также он всегда
сохраняется в `screenshots/`, независимо от того, используется ли Allure.

## Как всё это связано между собой

- **`site/`** — тестируемое приложение. Элементы содержат атрибуты
  `data-testid` (основной локатор для фреймворка) наряду с обычными `id`,
  классами и текстом ссылок — `site/README.md` показывает, где какую
  стратегию локаторов удобно тренировать.
- **`framework/pages/`** — классический Page Object Model: каждый класс
  страницы наследует `BasePage` (ожидания, клики, алерты, фреймы, окна)
  и предоставляет методы на языке бизнеса (`login_page.login(...)`,
  `cart_page.set_quantity(...)`), которые возвращают следующий Page Object —
  благодаря этому тесты читаются как сценарий действий пользователя, а не
  набор сырых вызовов Selenium.
- **`standalone_examples/`** намеренно обходится без слоя Page Object —
  каждый скрипт линеен и посвящён только одному API Selenium, чтобы сначала
  разобраться с примитивами, а уже потом прятать их за абстракциями.
- **`tests/`** — здесь всё соединяется: фикстуры pytest создают свежий
  браузер и Page Object'ы для каждого теста, а локальный HTTP-сервер
  (session-scope) отдаёт `site/`, так что тесты работают с настоящими
  `http://`-адресами.
- **`test_styles/`** — один и тот же сценарий логина 4 раза подряд, чтобы
  увидеть по отдельности, что даёт fixture, а что даёт Page Object, прежде
  чем встретить оба приёма уже смешанными в `tests/`.

## Как развивать проект дальше

Идеи для дальнейшей практики:
- Добавить `docker-compose.yml` с Selenium Grid / Selenoid и настроить
  `driver_factory.py` на Remote WebDriver.
- Добавить GitHub Actions workflow, который запускает
  `pytest --alluredir=allure-results` и публикует отчёт.
- Добавить визуальное регресс-тестирование (например, сравнивать
  скриншоты в духе `10_screenshots.py` с эталоном) на страницах каталога
  и товара.
- Параметризовать `test_product_page.py` по всем 6 id товаров вместо
  одного на тест — механика и пример разобраны в разделе «Параметризация» выше.
