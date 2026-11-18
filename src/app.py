import httpx
from rich.text import Text
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Input, Static

from link_validator import LinkValidator
from speed_tester import SpeedTester

REQUEST_COUNT = 10
INVALID_MESSAGE = "Ссылка недействительна, попробуйте снова."


class LinkTesterApp(App):
    CSS = """
    Screen { align: center middle; }
    #panel { width: 72; height: auto; border: round $primary; padding: 1 2; }
    #link_value { height: 1; margin-bottom: 1; }
    #buttons { height: 3; }
    #buttons Button { margin-right: 2; }
    #input_row { height: 3; margin-top: 1; visibility: hidden; }
    #link_input { width: 1fr; }
    #save { width: 16; margin-left: 1; }
    #message { height: 1; color: red; }
    #stats { height: 5; margin-top: 1; }
    """

    def __init__(self):
        super().__init__()
        self.link = None

    def compose(self) -> ComposeResult:
        with Vertical(id="panel"):
            yield Static("Ссылка: не задана", id="link_value")
            with Horizontal(id="buttons"):
                yield Button("Ссылка", id="link")
                yield Button("Тест", id="test", disabled=True)
                yield Button("Выход", id="exit")
            with Horizontal(id="input_row"):
                yield Input(placeholder="Вставьте ссылку сюда", id="link_input")
                yield Button("Сохранить", id="save", variant="success")
            yield Static("", id="message")
            yield Static("", id="stats")

    def on_button_pressed(self, event: Button.Pressed):
        button_id = event.button.id
        if button_id == "exit":
            self.exit()
        elif button_id == "link":
            self.open_link_menu()
        elif button_id == "save":
            self.save_link()
        elif button_id == "test":
            self.run_worker(self.run_test(), exclusive=True)

    def open_link_menu(self):
        link_input = self.query_one("#link_input", Input)
        self.query_one("#input_row").styles.visibility = "visible"
        link_input.value = ""
        self.query_one("#message", Static).update("")
        link_input.focus()

    def on_input_changed(self, event: Input.Changed):
        self.query_one("#message", Static).update("")

    def on_input_submitted(self, event: Input.Submitted):
        self.save_link()

    # Проверяет введённую ссылку, сохраняет её и включает кнопку Тест
    def save_link(self):
        value = self.query_one("#link_input", Input).value.strip()
        if not LinkValidator.is_valid(value):
            self.query_one("#message", Static).update(INVALID_MESSAGE)
            return
        self.link = value
        self.query_one("#link_value", Static).update(Text(f"Ссылка: {value}"))
        self.query_one("#test", Button).disabled = False
        self.query_one("#input_row").styles.visibility = "hidden"
        self.query_one("#link", Button).focus()

    def set_busy(self, busy):
        self.query_one("#link", Button).disabled = busy
        self.query_one("#test", Button).disabled = busy

    def show_progress(self, stats, current_request):
        self.query_one("#stats", Static).update(
            f"Запрос: {current_request}/{REQUEST_COUNT}\n"
            f"Получено данных: {stats.total_mb:.2f} МБ\n"
            f"Скорость: {stats.kb_per_second:.1f} КБ/с | {stats.mb_per_second:.2f} МБ/с\n"
            f"Среднее время запроса: {stats.average_time:.3f} с"
        )

    # Запускает весь тест и в конце всегда разблокирует кнопки
    async def run_test(self):
        self.set_busy(True)
        stats_widget = self.query_one("#stats", Static)
        stats_widget.update("Запуск...")
        tester = SpeedTester(self.link, REQUEST_COUNT, self.show_progress)
        try:
            await tester.run()
        except httpx.HTTPError as error:
            stats_widget.update(Text(f"Ошибка запроса: {error}"))
        finally:
            self.set_busy(False)