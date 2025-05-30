from .widget import Widget
from PyQt6.QtGui import QTextCursor, QColor, QTextCharFormat, QKeyEvent
from PyQt6.QtCore import Qt



class DropdownMenu(Widget):
    def __init__(self, console, label: str, min_val=30, max_val=130, step=10, initial=50):
        self.console = console
        self.label = label
        self.min = min_val
        self.max = max_val
        self.step = step
        self.value = initial
        self.active = True
        self.start_pos = 0
        
        self.formats = {
            'normal': self._create_format("#00FF00"),
            'inactive': self._create_format("#888888")
        }


    def _render(self):
        self._clear()
        cursor = self.console.textCursor()
        cursor.setPosition(self.get_start_pos())
        total_blocks = 10
        filled = int((self.value + self.min) / (self.max + self.min) * total_blocks)
        print(filled)
        bar = "[" + "■" * filled + "-" * (total_blocks - filled) + "]"
        slider = f"{self.label}: {bar} {self.value}%\n"
        if self.active:
            cursor.insertText(slider, self.formats['normal'])
        else:
            cursor.insertText(slider, self.formats['inactive'])
        self.console.setTextCursor(cursor)

    def handle_key(self, key: int) -> bool:
        if not self.active:
            return False
        if key == Qt.Key.Key_Left:
            self.value = max(self.min, self.value - self.step)
            self._render()
            return True
        elif key == Qt.Key.Key_Right:
            self.value = min(self.max, self.value + self.step)
            self._render()
            return True
        elif key == Qt.Key.Key_Return:
            self._select_item()
            return True
        elif key == Qt.Key.Key_Escape:
            self.remove()
            return True