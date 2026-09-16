# ShopEasy — демо-сайт

Небольшой интернет-магазин электроники без бэкенда — тестируемое приложение
для учебных занятий по Selenium/Pytest из этого репозитория. Всё построено
на статическом HTML + чистом JS; «хранилище данных» — `localStorage`
(корзина, сессия авторизации).

## Страницы

| Файл | Назначение | Элементы, на которых стоит потренироваться |
|---|---|---|
| `index.html` | Главная страница, витрина товаров, живой поиск | `#search-input`, `[data-testid=product-card]`, `#no-results-msg` |
| `catalog.html` | Полный каталог с фильтром по категории, ползунком цены и сортировкой | `#category-filter`, `#max-price` (range), `#sort-select`, `#result-count` |
| `product.html?id=1..6` | Страница товара | выпадающий список количества, `#add-to-cart-btn`, вкладки (`.tab-btn` / `.tab-panel`) |
| `login.html` | Форма входа | валидные данные: `test@example.com` / `Password123`; `#login-error` при ошибке |
| `register.html` | Форма регистрации | текст/email/пароль, радиокнопки (пол), select (страна), два чекбокса, поле даты, инлайн-ошибки валидации |
| `cart.html` | Таблица корзины | поле количества `<input type=number>` в каждой строке, кнопка удаления, пересчёт суммы на лету |
| `checkout.html` | Мастер оформления заказа в 3 шага | навигация по шагам, условные поля карты, нативный `confirm()` на «Оформить заказ» |
| `dashboard.html` | Личный кабинет (требует авторизации) | редирект на `login.html`, если не авторизован; таблица истории заказов; нативный `confirm()` при удалении аккаунта |
| `playground.html` | Набор «сложных» элементов для Selenium | см. таблицу ниже |
| `iframe_content.html` | Загружается внутри `<iframe>` на странице playground | `#iframe-input`, `#iframe-echo` |
| `new_tab.html` | Открывается через `target="_blank"` со страницы playground | используется для переключения между окнами |

## Карта виджетов `playground.html`

У каждого блока есть `data-testid` на контейнере, блоки не зависят друг от друга:

| Виджет | `data-testid` | Какую возможность Selenium отрабатывает |
|---|---|---|
| JS-диалоги | `widget-alerts` | `alert()`, `confirm()`, `prompt()` / `driver.switch_to.alert` |
| Iframe | `widget-iframe` | `driver.switch_to.frame(...)` |
| Drag and drop | `widget-dragdrop` | `ActionChains`, особенности HTML5 DnD (рекомендуется JS-фоллбэк) |
| Динамическая подгрузка | `widget-dynamic` | `WebDriverWait` / `expected_conditions` |
| Всплывающая подсказка при наведении | `widget-tooltip` | `ActionChains.move_to_element` |
| Новая вкладка | `widget-newtab` | `driver.window_handles`, `switch_to.window` |
| Загрузка файла | `widget-upload` | `input.send_keys(path)` |
| Мультиселект | `widget-multiselect` | `selenium.webdriver.support.ui.Select` |
| Сортируемая таблица | `widget-table` | чтение строк/ячеек `<table>`, повторное чтение после изменений DOM (staleness) |
| Ползунок диапазона | `widget-slider` | стрелки клавиатуры / выставление значения через JS + событие `input` |
| Переключатель enable/disable | `widget-toggle` | ожидание, пока элемент станет кликабельным |

## Заметки о стратегиях локаторов (для обучения)

Разметка намеренно предоставляет несколько способов найти один и тот же
элемент, чтобы на тестах можно было отрабатывать разные стратегии:
- `data-testid="..."` — стратегия по умолчанию для Page Object'ов (стабильная, явная).
- `id="..."` — используется для полей форм.
- Обычные CSS-классы (`.product-card`, `.tab-btn`) — используются в паре тестов/примеров, чтобы показать `By.CSS_SELECTOR` / `By.CLASS_NAME`.
- Обычный текст ссылок (например, «Create one», «Back to catalog») — используется для показа `By.LINK_TEXT` / `By.PARTIAL_LINK_TEXT`.

## Запуск сайта отдельно

Сборка не нужна. Варианты:
- Открыть любой `.html`-файл прямо в браузере (`file://...`), либо
- Раздать папку через сервер, чтобы относительные ссылки и iframe вели себя как в реальном деплое:

```bash
python -m http.server 8000 --directory site
```

Pytest-фреймворк в `tests/` поднимает такой сервер автоматически
(см. `framework/utils/local_server.py`), так что вручную запускать его
для автотестов не нужно.
