from .widget import Widget
from PyQt6.QtGui import QTextCursor, QColor, QTextCharFormat, QKeyEvent
from PyQt6.QtCore import Qt


class CheckboxHorizontal:
    def __init__(self, console, options: list):
        self.console = console
        self.options = options
        self.checked = [False] * len(options)
        self.selected = 0
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

        for i, option in enumerate(self.options):
            fmt = (
                self.formats['selected'] if self.active and i == self.selected
                else self.formats['normal'] if self.active
                else self.formats['inactive']
            )
            checkbox = "[X]" if self.checked[i] else "[ ]"
            cursor.insertText(f"{checkbox} {option}", fmt)
            if i != len(self.options) - 1:
                cursor.insertText("   ")
        cursor.insertText("\n")
        self.console.setTextCursor(cursor)
        



    def handle_key(self, key: int) -> bool:
        if not self.active:
            return False

        if key == Qt.Key.Key_Left:
            self.selected = max(0, self.selected - 1)
            self._render()
            return True
        elif key == Qt.Key.Key_Right:
            self.selected = min(len(self.options) - 1, self.selected + 1)
            self._render()
            return True
        elif key == Qt.Key.Key_Space:
            self.checked[self.selected] = not self.checked[self.selected]
            self._render()
            return True
        elif key == Qt.Key.Key_Return:
            selected_items = [self.options[i] for i, val in enumerate(self.checked) if val]
            self._select_item(selected_items)
            return True
        elif key == Qt.Key.Key_Escape:
            self.remove()
            return True
        return False


    def _select_item(self, result):
        print(result)
        self.remove()

    def stop(self):
        pass








class CheckboxVertical:
    def __init__(self, console, options: list):
        self.console = console
        self.options = options
        self.checked = [False] * len(options)
        self.selected = 0
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

        for i, option in enumerate(self.options):
            fmt = (
                self.formats['selected'] if self.active and i == self.selected
                else self.formats['normal'] if self.active
                else self.formats['inactive']
            )
            checkbox = "[X]" if self.checked[i] else "[ ]"
            cursor.insertText(f"{checkbox} {option}", fmt)
            if i != len(self.options) - 1:
                cursor.insertText("\n")
        cursor.insertText("\n")
        self.console.setTextCursor(cursor)
        



    def handle_key(self, key: int) -> bool:
        if not self.active:
            return False

        if key == Qt.Key.Key_Up:
            self.selected = max(0, self.selected - 1)
            self._render()
            return True
        elif key == Qt.Key.Key_Down:
            self.selected = min(len(self.options) - 1, self.selected + 1)
            self._render()
            return True
        elif key == Qt.Key.Key_Space:
            self.checked[self.selected] = not self.checked[self.selected]
            self._render()
            return True
        elif key == Qt.Key.Key_Return:
            selected_items = [self.options[i] for i, val in enumerate(self.checked) if val]
            self._select_item(selected_items)
            return True
        elif key == Qt.Key.Key_Escape:
            self.remove()
            return True
        return False


    def _select_item(self, result):
        print(result)
        self.remove()

    def stop(self):
        pass