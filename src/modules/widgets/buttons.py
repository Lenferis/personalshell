from .widget import Widget
from PyQt6.QtGui import QTextCursor, QColor, QTextCharFormat, QKeyEvent
from PyQt6.QtCore import Qt

class ButtonVertical(Widget):
    def __init__(self, console, options: list, stop_method):
        super().__init__(console, stop_method=stop_method)
        self.options = options
        self.selected = 0
        self.active = True
        self.start_pos = 0

        self.formats = {
            'normal': self._create_format("#00FF00"),
            'selected': self._create_format("#FFFFFF", "#004400"),
            'inactive': self._create_format("#888888")
        }

    def _render(self):
        self._clear()
        cursor = self.console.textCursor()
        cursor.setPosition(self.get_start_pos())
        for i, label in enumerate(self.options):
            if self.active:
                fmt = self.formats['selected'] if i == self.selected else self.formats['normal']
                cursor.insertText(f"[ {label} ]\n", fmt)
            else:
                fmt = self.formats['inactive']
                cursor.insertText(f"[ {label} ]\n", fmt)
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
        elif key == Qt.Key.Key_Return:
            self._select_item(self.options[self.selected])
            return True
        elif key == Qt.Key.Key_Escape:
            self.remove()
            return True

class ButtonHorizontal(Widget):
    def __init__(self, console, options: list):
        super().__init__(console)
        self.options = options
        self.selected = 0
        self.active = True
        self.start_pos = 2
        
        self.formats = {
            'normal': self._create_format("#00FF00"),
            'selected': self._create_format("#FFFFFF", "#004400"),
            'inactive': self._create_format("#888888")
        }

    def create_start_pos(self):
        self.console.append("")
        self.start_block = self.console.document().blockCount() - 1

    def _create_format(self, fg, bg=None):
        fmt = QTextCharFormat()
        fmt.setForeground(QColor(fg))
        if bg:
            fmt.setBackground(QColor(bg))
        return fmt

    def show(self):
        self.create_start_pos()
        self._render()
    
    def get_start_pos(self):
        doc = self.console.document()
        block = doc.findBlockByLineNumber(self.start_block)
        return block.position()

    def _clear(self):
        cursor = self.console.textCursor()
        cursor.setPosition(self.get_start_pos())
        cursor.movePosition(QTextCursor.MoveOperation.End, QTextCursor.MoveMode.KeepAnchor)
        cursor.removeSelectedText()
        self.console.setTextCursor(cursor)

    def _render(self):
        self._clear()
        cursor = self.console.textCursor()
        cursor.setPosition(self.get_start_pos())
        for i, label in enumerate(self.options):
            if self.active:
                fmt = self.formats['selected'] if i == self.selected else self.formats['normal']
                cursor.insertText(f"[ {label} ]", fmt)
            else:
                fmt = self.formats['inactive']
                cursor.insertText(f"[ {label} ]", fmt)
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
        elif key == Qt.Key.Key_Return:
            self._select_item(self.options[self.selected])
            return True
        elif key == Qt.Key.Key_Escape:
            self.remove()
            return True

    def deactivate(self):
        self.active = False
        self._render()
        if self.console.active_widgets == self:
            self.console.active_widgets = None

        cursor = self.console.textCursor()
        cursor.setCharFormat(QTextCharFormat())
        cursor.insertText(f"> ")

    def remove(self, result):
        self._clear()
        if self.console.active_widgets == self:
            self.console.active_widgets = None
        self.console.show_prompt()

    def _select_item(self):
        self.remove()

    