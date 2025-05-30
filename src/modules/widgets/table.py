from .widget import Widget
from PyQt6.QtGui import QTextCursor, QColor, QTextCharFormat, QKeyEvent
from PyQt6.QtCore import Qt

class DropdownMenu:
    def __init__(self, console, headers, data):
        self.console = console
        self.headers = headers
        self.data = data
        self.rows = len(data)
        self.cols = len(headers)
        self.row = 0
        self.col = 0
        self.active = True
        self.start_pos = 0
        
        self.formats = {
            'header': self._create_format("#496349"),
            'selected': self._create_format("#00FF00"),
            'normal': self._create_format("#966565")
        }

    def _render(self):
        self._clear()
        cursor = self.console.textCursor()
        cursor.setPosition(self.get_start_pos())

        col_widths = [max(len(str(row[i])) for row in self.data) for i in range(self.cols)]
        col_widths = [max(col_widths[i], len(self.headers[i])) + 2 for i in range(self.cols)]
        def fmt_cell(text, width):
            return f"{str(text):<{width}}"

        header_row = "".join(fmt_cell(self.headers[i], col_widths[i]) for i in range(self.cols)) + "\n"
        cursor.insertText(header_row, self.formats['header'])

        for r in range(self.rows):
            for c in range(self.cols):
                text = fmt_cell(self.data[r][c], col_widths[c])
                if r == self.row and c == self.col and self.active:
                    cursor.insertText(text, self.formats['selected'])
                else:
                    cursor.insertText(text, self.formats['normal'])
            cursor.insertText("\n")
        self.console.setTextCursor(cursor)
        



    def handle_key(self, key: int) -> bool:
        if not self.active:
            return False

        moved = False
        if key == Qt.Key.Key_Left:
            self.col = max(0, self.col - 1)
            moved = True
        elif key == Qt.Key.Key_Right:
            self.col = min(self.cols - 1, self.col + 1)
            moved = True
        elif key == Qt.Key.Key_Up:
            self.row = max(0, self.row - 1)
            moved = True
        elif key == Qt.Key.Key_Down:
            self.row = min(self.rows - 1, self.row + 1)
            moved = True
        elif key == Qt.Key.Key_Return:
            self._select_item(self.data[self.row][self.col])
            self.deactivate()
            self.console._add_prompt()
            return True
        elif key == Qt.Key.Key_Escape:
            self.remove()
            return True

        if moved:
            self._render()
            return True
        return False

    def deactivate(self):
        self.active = False
        self._render()
        if self.console.widget == self:
            self.console.widget = None

        cursor = self.console.textCursor()
        cursor.setCharFormat(QTextCharFormat())
        cursor.insertText(f"> ")

    def remove(self):
        self._clear()
        if self.console.widget == self:
            self.console.widget = None
        self.console.show_prompt()

    def _select_item(self, result):
        print(result)
        self.remove()

    def stop(self):
        pass