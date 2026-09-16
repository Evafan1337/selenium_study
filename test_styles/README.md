# test_styles — один сценарий, четыре уровня абстракции

Не часть основного набора `tests/` и не собирается обычной командой `pytest`
(`pytest.ini` ограничивает автосбор папкой `tests/` через `testpaths`) —
это отдельная учебная площадка, запускается только явным указанием пути.

Во всех четырёх файлах проверяется **один и тот же** сценарий логина:
успешный вход по верным данным и сообщение об ошибке по неверным. Меняется
только то, **как** устроен тест — постепенно добавляются fixtures и Page
Object, по одной идее за раз, чтобы было видно, что именно каждая из них
решает.

| Файл | Driver | Абстракция страницы | Что показывает |
|---|---|---|---|
| `test_01_raw_driver_no_fixtures.py` | создаётся вручную в каждом тесте, `webdriver.Chrome()` напрямую | нет — голые `By.*` | Боль: дублирование setup/teardown, и если `assert` упадёт — браузер останется висеть |
| `test_02_raw_driver_with_fixtures.py` | из fixture (`yield`), через `framework.utils.driver_factory` | нет — голые `By.*` | Fixtures решают проблему дублирования и гарантированной уборки, но локаторы и клики всё ещё в тексте теста |
| `test_03_page_object_no_fixtures.py` | создаётся вручную в каждом тесте, через `framework.utils.driver_factory` | `LoginPage`/`DashboardPage` из `framework/pages` | Page Object решает читаемость теста, но НЕ решает дублирование setup/teardown — эта боль всё ещё тут |
| `test_04_page_object_with_fixtures.py` | из fixture (`yield`), через `framework.utils.driver_factory` | `LoginPage`/`DashboardPage` из `framework/pages` | Обе идеи вместе — ровно так устроены `tests/conftest.py` и `tests/test_login.py` в этом проекте |

`test_01` нарочно не использует вообще ничего из `framework/` — ни `driver_factory`,
ни `local_server` — только `selenium` и `pytest`. Страница логина открывается
напрямую с диска (`file://...`), браузер — всегда видимый Chrome без headless,
пауза между действиями зашита прямо в файл как `SLEEP_SECONDS = 3` (см. сам
файл). Это самый голый вариант из всех четырёх — специально, чтобы было на
чём наглядно демонстрировать: `pytest test_styles/test_01_raw_driver_no_fixtures.py -v -s`
запускается вообще без знания о существовании `framework/`.

## Запуск

```bash
# все четыре файла разом
pytest test_styles/ -v

# один конкретный уровень
pytest test_styles/test_02_raw_driver_with_fixtures.py -v

# демка: видимый браузер, -s чтобы видеть print(), ~35 секунд из-за пауз в 3с
pytest test_styles/test_01_raw_driver_no_fixtures.py -v -s
```

## На что смотреть

1. Откройте `test_01` и `test_02` рядом — посчитайте строки внутри самих
   функций `test_successful_login`. Разница — это то, что даёт fixture.
2. Откройте `test_01` и `test_03` рядом — здесь разница в чтении теста
   («сценарий пользователя» против «список вызовов Selenium»), а вот
   повторяющийся setup/teardown остался — Page Object эту боль не лечит.
3. `test_04` решает обе проблемы сразу — и это ровно то, что уже сделано
   в `tests/` для всего остального проекта. Дальше в `tests/conftest.py`
   те же самые `driver` и `site_server` просто переиспользуются десятками
   тестов вместо того, чтобы объявляться в каждом файле заново.
4. `test_01` вообще не знает про `framework/` — это не только про fixtures
   и Page Object, а ещё и про то, что `pytest` умеет запускать буквально
   что угодно с функцией `test_*`, без единой зависимости от остального
   проекта. `test_02`–`test_04` уже используют `framework.utils.driver_factory`
   и `LocalSiteServer` — сравните, что именно это добавляет (настраиваемость
   через `HEADLESS`/`BROWSER`, реальный `http://`-адрес вместо `file://`).
