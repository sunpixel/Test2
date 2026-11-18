# Link Speed Tester

[English](#english) | [Русский](#русский)

---

## English

### Overview

Link Speed Tester is a small console application with a text interface (TUI). You give it a link to a file or an image, and it downloads that link several times in a row and shows how fast your connection is: the amount of data received, the download speed and the average request time.

The interface of the program is in Russian.

### Requirements

- Python 3.9 or newer
- Libraries: `textual` and `httpx`

### Installation and launch

Python is an interpreted language, so there is nothing to compile. Installing the dependencies is the only preparation.

1. Put all project files into one folder.
2. Open a terminal in that folder.
3. (Optional) Create and activate a virtual environment:

```
python -m venv venv
venv\Scripts\activate
```

On Linux and macOS the activation command is:

```
source venv/bin/activate
```

4. Install the dependencies:

```
pip install textual httpx
```

5. Run the program:

```
python main.py
```

To leave the virtual environment, run `deactivate`.

### Project structure

| File | Purpose |
|---|---|
| `main.py` | Entry point. Contains the `Main` function that starts the app. |
| `app.py` | The `LinkTesterApp` class: the interface, buttons and their logic. |
| `link_validator.py` | The `LinkValidator` class: checks that a link is valid. |
| `speed_tester.py` | The `SpeedTester` class: sends the requests and measures the time. |
| `download_stats.py` | The `DownloadStats` class: stores the results and calculates the averages and speed. |

How the modules work together:

1. `main.py` creates `LinkTesterApp` and starts it.
2. When you save a link, `app.py` asks `LinkValidator` whether the link is valid.
3. When you press the test button, `app.py` creates a `SpeedTester` and runs it.
4. `SpeedTester` downloads the link and fills a `DownloadStats` object. During the download it regularly calls back into `app.py`, which redraws the numbers on the screen.

### Interface

The whole program is one framed panel. From top to bottom:

```
┌──────────────────────────────────────────────┐
│ Ссылка: https://example.com/file.zip         │  link line
│                                              │
│ [ Ссылка ]  [ Тест ]  [ Выход ]              │  buttons
│                                              │
│ [ Paste a link here        ] [ Сохранить ]   │  input row
│ Ссылка недействительна, попробуйте снова.    │  error line
│                                              │
│ Запрос: 2/5                                  │
│ Получено данных: 48.20 МБ                    │  statistics
│ Скорость: 20480.0 КБ/с | 20.00 МБ/с          │
│ Среднее время запроса: 1.210 с               │
└──────────────────────────────────────────────┘
```

- **Link line.** Shows the saved link, or `Ссылка: не задана` ("Link: not set") if there is none yet.
- **Ссылка (Link) button.** Opens the input row so you can type or paste a link.
- **Тест (Test) button.** Starts the speed test. It is inactive until a valid link is saved, and it is locked while a test is running.
- **Выход (Exit) button.** Closes the program. `Ctrl+Q` does the same.
- **Input row.** Hidden until you press **Ссылка**. It holds the text field and the **Сохранить** (Save) button. Pressing Enter in the field works like pressing Save.
- **Error line.** If the link is not valid, it shows `Ссылка недействительна, попробуйте снова.` ("Link is not valid, try again."). The message disappears as soon as you start typing. The layout never moves, because every area has a fixed place.
- **Statistics.** Updated live during the test.

### How to use

1. Press **Ссылка**.
2. Paste or type a link and press **Сохранить** (or Enter).
3. If the link is valid, it appears at the top and **Тест** becomes active. If not, fix the link and try again.
4. Press **Тест** and watch the statistics.
5. Press **Выход** to close the program.

A valid link starts with `http://` or `https://`, has no spaces and has a host name with a dot (or is `localhost`).

For a meaningful result, use a large file. A good option is `https://speed.cloudflare.com/__down?bytes=25000000` (25 MB). Small files finish too fast to measure the speed properly.

### Units and how they are calculated

| Value | Unit | How it is calculated |
|---|---|---|
| Data received | MB (МБ) | Total bytes of all responses divided by 1024 × 1024 |
| Speed | KB/s (КБ/с) | Total bytes divided by total download time, then divided by 1024 |
| Speed | MB/s (МБ/с) | Total bytes divided by total download time, then divided by 1024 × 1024 |
| Average request time | seconds (с) | Sum of the times of all finished requests divided by their count |
| Request counter | pieces | Current request number out of the total |

Notes:

- 1 KB = 1024 bytes and 1 MB = 1024 KB, as in most file managers.
- Each request is sent only after the previous one is fully downloaded, and its time is counted from the start of the request until the last byte arrives.
- During the test the speed is recalculated about 10 times per second.
- The number of requests is set by `REQUEST_COUNT` at the top of `app.py` (5 by default).
- Speed is shown in bytes, not bits. To get megabits per second, multiply MB/s by 8.

### Troubleshooting

- **`ModuleNotFoundError`**: the dependencies are not installed. Run `pip install textual httpx`.
- **`Ошибка запроса: ...` (Request failed)**: the server is not reachable, the link is broken or the server returned an error. Check the link in a browser.
- **The terminal is stuck**: press `Ctrl+C`.

---

## Русский

### Обзор

Link Speed Tester — небольшое консольное приложение с текстовым интерфейсом (TUI). Вы указываете ссылку на файл или изображение, а программа несколько раз подряд скачивает её и показывает скорость вашего соединения: объём полученных данных, скорость загрузки и среднее время запроса.

### Требования

- Python 3.9 или новее
- Библиотеки: `textual` и `httpx`

### Установка и запуск

Python — интерпретируемый язык, поэтому компилировать ничего не нужно. Вся подготовка сводится к установке зависимостей.

1. Положите все файлы проекта в одну папку.
2. Откройте терминал в этой папке.
3. (По желанию) Создайте и активируйте виртуальное окружение:

```
python -m venv venv
venv\Scripts\activate
```

В Linux и macOS команда активации такая:

```
source venv/bin/activate
```

4. Установите зависимости:

```
pip install textual httpx
```

5. Запустите программу:

```
python main.py
```

Чтобы выйти из виртуального окружения, выполните `deactivate`.

### Структура проекта

| Файл | Назначение |
|---|---|
| `main.py` | Точка входа. Содержит функцию `Main`, которая запускает приложение. |
| `app.py` | Класс `LinkTesterApp`: интерфейс, кнопки и их логика. |
| `link_validator.py` | Класс `LinkValidator`: проверяет, что ссылка корректна. |
| `speed_tester.py` | Класс `SpeedTester`: отправляет запросы и измеряет время. |
| `download_stats.py` | Класс `DownloadStats`: хранит результаты, считает среднее и скорость. |

Как модули работают вместе:

1. `main.py` создаёт `LinkTesterApp` и запускает его.
2. При сохранении ссылки `app.py` спрашивает у `LinkValidator`, корректна ли она.
3. При нажатии кнопки теста `app.py` создаёт `SpeedTester` и запускает его.
4. `SpeedTester` скачивает ссылку и заполняет объект `DownloadStats`. Во время загрузки он регулярно вызывает функцию из `app.py`, которая обновляет цифры на экране.

### Интерфейс

Вся программа — одна панель в рамке. Сверху вниз:

```
┌──────────────────────────────────────────────┐
│ Ссылка: https://example.com/file.zip         │  строка со ссылкой
│                                              │
│ [ Ссылка ]  [ Тест ]  [ Выход ]              │  кнопки
│                                              │
│ [ Вставьте ссылку сюда     ] [ Сохранить ]   │  строка ввода
│ Ссылка недействительна, попробуйте снова.    │  строка ошибки
│                                              │
│ Запрос: 2/5                                  │
│ Получено данных: 48.20 МБ                    │  статистика
│ Скорость: 20480.0 КБ/с | 20.00 МБ/с          │
│ Среднее время запроса: 1.210 с               │
└──────────────────────────────────────────────┘
```

- **Строка со ссылкой.** Показывает сохранённую ссылку или `Ссылка: не задана`, если её ещё нет.
- **Кнопка «Ссылка».** Открывает строку ввода, где можно напечатать или вставить ссылку.
- **Кнопка «Тест».** Запускает проверку скорости. Пока нет корректной сохранённой ссылки, кнопка неактивна, а во время теста она блокируется.
- **Кнопка «Выход».** Закрывает программу. `Ctrl+Q` делает то же самое.
- **Строка ввода.** Скрыта, пока вы не нажмёте «Ссылка». Содержит поле ввода и кнопку «Сохранить». Enter в поле работает так же, как нажатие «Сохранить».
- **Строка ошибки.** Если ссылка некорректна, здесь появляется `Ссылка недействительна, попробуйте снова.` Сообщение исчезает, как только вы начинаете печатать. Интерфейс не «прыгает», потому что у каждой области фиксированное место.
- **Статистика.** Обновляется в реальном времени во время теста.

### Как пользоваться

1. Нажмите «Ссылка».
2. Вставьте или напечатайте ссылку и нажмите «Сохранить» (или Enter).
3. Если ссылка корректна, она появится сверху, а кнопка «Тест» станет активной. Если нет — исправьте ссылку и попробуйте снова.
4. Нажмите «Тест» и наблюдайте за статистикой.
5. Нажмите «Выход», чтобы закрыть программу.

Корректная ссылка начинается с `http://` или `https://`, не содержит пробелов и имеет имя хоста с точкой (либо это `localhost`).

Для осмысленного результата берите большой файл. Хороший вариант: `https://speed.cloudflare.com/__down?bytes=25000000` (25 МБ). Маленькие файлы скачиваются слишком быстро, и скорость не удаётся измерить как следует.

### Единицы измерения и как они считаются

| Величина | Единица | Как считается |
|---|---|---|
| Получено данных | МБ | Сумма байт всех ответов, делённая на 1024 × 1024 |
| Скорость | КБ/с | Всего байт, делённое на общее время загрузки, затем на 1024 |
| Скорость | МБ/с | Всего байт, делённое на общее время загрузки, затем на 1024 × 1024 |
| Среднее время запроса | секунды (с) | Сумма времени всех завершённых запросов, делённая на их количество |
| Счётчик запросов | штуки | Номер текущего запроса из общего числа |

Примечания:

- 1 КБ = 1024 байта, а 1 МБ = 1024 КБ, как в большинстве файловых менеджеров.
- Каждый запрос отправляется только после полной загрузки предыдущего, а его время считается от начала запроса до прихода последнего байта.
- Во время теста скорость пересчитывается примерно 10 раз в секунду.
- Количество запросов задаётся константой `REQUEST_COUNT` в начале файла `app.py` (по умолчанию 5).
- Скорость показана в байтах, а не в битах. Чтобы получить мегабиты в секунду, умножьте МБ/с на 8.

### Возможные проблемы

- **`ModuleNotFoundError`**: зависимости не установлены. Выполните `pip install textual httpx`.
- **`Ошибка запроса: ...`**: сервер недоступен, ссылка сломана или сервер вернул ошибку. Проверьте ссылку в браузере.
- **Терминал завис**: нажмите `Ctrl+C`.
