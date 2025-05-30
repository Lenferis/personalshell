from .widget import Widget
from PyQt6.QtGui import QTextCursor, QColor, QTextCharFormat, QKeyEvent
from PyQt6.QtCore import Qt


class SearchListWidget(Widget):
    def __init__(self, console, items):
        self.console = console
        self.items = items
        self.filtered_items = items
        self.page = 0
        self.items_per_page = 10
        self.query = ""
        self.selected_index = 0
        self.active = True


        self.formats = {
            'query': self._create_format("#00D9FF"),
            'normal': self._create_format("#00FF00"),
            'selected': self._create_format("#FFFFFF", "#004400"),
            'inactive': self._create_format("#888888")
        }

    def _render(self):
        self._clear()
        cursor = self.console.textCursor()
        cursor.setPosition(self.get_start_pos())

        cursor.insertText(f"Search: {self.query}_\n", self.formats['query'])
        start = self.page * self.items_per_page
        end = start + self.items_per_page
        for i, item in enumerate(self.filtered_items[start:end]):
            global_index = start + i
            cursor.insertText(f"{'>' if global_index == self.selected_index else ''} {item}\n", self.formats['selected'] if global_index == self.selected_index else self.formats['normal'] )

        total_pages = max(1, (len(self.filtered_items) - 1) // self.items_per_page + 1)
        cursor.insertText(f"{self.page + 1} \ {total_pages}\n", self._create_format("gray"))
        self.console.setTextCursor(cursor)
    def handle_key(self, event):
        if not self.active:
            return False
        key = event.key()
        text = event.text()
        if key == Qt.Key.Key_Escape:
            self.remove()
            return True
        elif key == Qt.Key.Key_Backspace:
            self.query = self.query[:-1]
            self._filter()
        elif key == Qt.Key.Key_Return:
            selected_item = self.filtered_items[self.selected_index]
            print(selected_item)

            return True
        elif key == Qt.Key.Key_Left:
            self.page = max(0, self.page - 1)
            self.selected_index = self.page * self.items_per_page
        elif key == Qt.Key.Key_Right:
            max_page = max(0, (len(self.filtered_items) - 1) // self.items_per_page)
            self.page = min(max_page, self.page + 1)
            self.selected_index = self.page * self.items_per_page
        elif key == Qt.Key.Key_Up:
            self.selected_index = max(0, self.selected_index - 1)
            self.page = self.selected_index // self.items_per_page
        elif key == Qt.Key.Key_Down:
            self.selected_index = min(len(self.filtered_items) - 1, self.selected_index + 1)
            self.page = self.selected_index // self.items_per_page
        else:
            self.query += text
            self._filter()

        self._render()
        return True

    def _filter(self):
        self.filtered_items = [item for item in self.items if self.query.lower() in item.lower()]
        self.page = 0
        self.cursor_index = 0
        if not self.filtered_items:
            self.filtered_items = ["(ничего не найдено)"]