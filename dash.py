from textual.app import App, ComposeResult
from textual.widgets import (
    DataTable, Footer,
    Button, Static, Input)
from textual.containers import Container
from textual.screen import Screen
from engine import Connector
import datetime
import webbrowser
import io
import csv


class NewTask(Static):
    def compose(self) -> ComposeResult:
        yield Input(placeholder="URL", id="url")
        yield Input(placeholder="Note", id="note")
        yield Button("ADD", id="add", variant="success")


class Task(Static):

    def __init__(self, _id, _url, _itemCount, _note, _lastchecked, _status):
        Static.__init__(self)
        self._id = _id
        self._url = _url
        self._itemCount = _itemCount
        self._note = _note
        self._lastchecked = _lastchecked
        self._status = _status

    def compose(self) -> ComposeResult:
        yield Static(self._id, id="_id")
        yield Static(f"[@click=app.browse_link('{self._url}')]CLICK HERE[/]", id="_url")
        yield Static(self._itemCount, id="_itemcount")
        yield Static(self._status, id="_status")
        yield Static(self._lastchecked, id="lcheck")
        yield Static(f"[@click=app.load_items('{self._id}')]"
                     f"{self._note}[/]", id="_note")
        yield Button("Enable", id="changeStatus", variant="success")
        yield Button("Delete", id="delete")


class TaskList(Static):

    def compose(Static) -> ComposeResult:
        db = Connector("db.sqlite3")
        data = db.getTasks()
        for d in data:
            count = db.getItemCount(d[0])
            yield Task(
                _id=str(d[0]),
                _url=d[1],
                _itemCount=str(count),
                _note=d[3],
                _lastchecked=d[4],
                _status=d[2]
            )


class ItemsScreen(Screen):
    BINDINGS = [("escape", "app.close_scr", "Return")]

    def __init__(self, taskID):
        Screen.__init__(self)
        self.taskID = taskID

    def writeio(self, data):
        iofile = io.StringIO()
        iofile.write("Title,Condition,Price,Purchase,Shipping,URL\n")
        for d in data[:10]:
            line = ",".join([x.replace(",", "") for x in d]).replace("\n", "")
            iofile.write(line + "\n")
        iofile.seek(0)
        return iofile

    def compose(self) -> ComposeResult:
        yield Footer()
        yield DataTable()

    def on_mount(self) -> None:
        db = Connector("db.sqlite3")
        data = db.getItems(self.taskID)
        table = self.query_one(DataTable)
        rows = csv.reader(self.writeio(data))
        table.add_columns(*next(rows))
        table.add_rows(rows)


class MainScreen(Screen):
    BINDINGS = [("d", "toggle_dark", "Display Mode")]

    def compose(self) -> ComposeResult:
        yield Footer()
        yield NewTask("NewTask")
        yield Container(TaskList(id="TaskList"))


class DashBoard(App):

    CSS_PATH = "dash.css"

    def on_mount(self) -> None:
        self.install_screen(MainScreen(), name="mainscr")
        self.push_screen("mainscr")

    def action_browse_link(self, url):
        webbrowser.open(url)

    def action_load_items(self, tid):
        self.install_screen(ItemsScreen(tid), name="itemscr")
        self.push_screen("itemscr")

    def action_close_scr(self):
        self.pop_screen()
        self.uninstall_screen("itemscr")
        self.push_screen("mainscr")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        db = Connector("db.sqlite3")
        if event.button.id == "add":
            lastC = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            url = self.query_one("NewTask").get_child_by_id("url").value
            note = self.query_one("NewTask").get_child_by_id("note").value
            dt = db.addTask([url, "ACTIVE", note, lastC])
            newTask = Task(
                _id=str(dt[0]),
                _url=dt[1],
                _itemCount="0",
                _lastchecked=dt[4],
                _status=dt[2],
                _note=dt[3]
            )
            self.query_one("TaskList").mount(newTask)
        elif event.button.id == "delete":
            task = event.button.parent
            db.removeTask(task._id)
            task.remove()

    def on_data_table_cell_highlighted(self, cell):
        if "https://www.ebay.com/itm/" in cell.value:
            webbrowser.open(cell.value)
        elif cell.value == "X":
            cell.remove()


if __name__ == "__main__":
    app = DashBoard()
    app.run()
