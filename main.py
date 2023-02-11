from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Static
from textual.containers import Container


class TimeDisplay(Static):
    pass


class StopWatch(Static):
    def compose(self) -> ComposeResult:
        yield Button("Start", id="start", variant="success")
        yield Button("Stop", id="stop", variant="error")
        yield Button("Reset", id='reset')
        yield TimeDisplay("00:00:00.00")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "start":
            self.add_class("started")
        elif event.button.id == "stop":
            self.remove_class("started")


class StopwatchApp(App):
    CSS_PATH = "stopwatch.css"
    BINDINGS = [("d", "toggle_dark", "Toggle Dark mode"),
                ("a", "add_stopwatch", "Add"),
                ("r", "remove_stopwatch", "Remove")
                ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True, name="Chronometer")
        yield Footer()
        yield Container(StopWatch(), StopWatch(), StopWatch(), id="timers")

    def action_add_stopwatch(self) -> None:
        new_st = StopWatch()
        self.query_one("#timers").mount(new_st)

    def action_remove_stopwatch(self) -> None:
        timers = self.query("StopWatch")
        if timers:
            timers.last().remove()

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark


if __name__ == "__main__":
    app = StopwatchApp()
    app.run()
