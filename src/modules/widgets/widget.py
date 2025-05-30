from PyQt6.QtGui import QTextCursor, QMouseEvent, QColor, QTextCharFormat, QKeyEvent
from PyQt6.QtCore import Qt

class Widget:
    def __init__(self, console):
        self.console = console
        self.start_pos = 0
        self.formats = {
            # 'normal': self._create_format("#00FF00")
        }

        self.stop_methods = {
            "deactivate": self.deactivate,
            "remove": self.remove,
            "hide": self.hide
        }
        self.stop_metod = ""

        self.active = True
        
    def create_start_pos(self):
        self.console.append("")
        self.start_pos = self.console.document().blockCount() - 1

    def print_promt(self):
        if self.stop_method == self.deactivate:
            cursor = self.console.textCursor()
            cursor.setCharFormat(QTextCharFormat())
            cursor.insertText(f"> ")
        else:
            cursor = self.console.textCursor()
            cursor.setCharFormat(QTextCharFormat())
            cursor.insertText(f"\n> ")
    
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
        block = doc.findBlockByLineNumber(self.start_pos)
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

    def handle_key(self, key: int) -> bool:
        if not self.active:
            return False
    def deactivate(self):
        self.active = False
        self._render()
        self.print_promt()
        del self

    def remove(self):
        self.active = False
        self._clear()
        self.print_promt()
        del self
    def hide(self):
        self.active = False
        self._clear()
        self.print_promt()

    def _select_item(self, result):
        pass

    def stop(self, stop_metod="remove"):
        self.stop_method = stop_metod
        if self.console.widget == self:
            self.console.widget = None
        if stop_metod:
            self.stop_methods[stop_metod]()



# class DropdownMenu:
#     def __init__(self, console, options: list):
#         self.console = console
#         self.options = options
#         self.selected = 0
#         self.active = True
#         self.menu_start_pos = 2
        
#         self.formats = {
#             'normal': self._create_format("#00FF00"),
#             'selected': self._create_format("#FFFFFF", "#004400"),
#             'inactive': self._create_format("#888888")
#         }
#     def start_pos(self):
#         self.console.append("")
#         self.start_block = self.console.document().blockCount() - 1

#     def _create_format(self, fg, bg=None):
#         fmt = QTextCharFormat()
#         fmt.setForeground(QColor(fg))
#         if bg:
#             fmt.setBackground(QColor(bg))
#         return fmt

#     def show(self):
#         self.start_pos()
#         self._render()
    
#     def get_start_pos(self):
#         doc = self.console.document()
#         block = doc.findBlockByLineNumber(self.start_block)
#         return block.position()

#     def _clear(self):
#         cursor = self.console.textCursor()
#         cursor.setPosition(self.get_start_pos())
#         cursor.movePosition(QTextCursor.MoveOperation.End, QTextCursor.MoveMode.KeepAnchor)
#         cursor.removeSelectedText()
#         self.console.setTextCursor(cursor)

#     def _render(self):
#         self._clear()
#         cursor = self.console.textCursor()
#         cursor.setPosition(self.get_start_pos())
#         for i, option in enumerate(self.options):
#             if self.active:
#                 fmt = self.formats['selected'] if i == self.selected else self.formats['normal']
#                 cursor.insertText(f"{'> ' if i == self.selected else '  '}{option}\n", fmt)
#             else:
#                 fmt = self.formats['inactive']
#                 cursor.insertText(f"  {option}\n", fmt)
#         self.console.setTextCursor(cursor)

#     def handle_key(self, key: int) -> bool:
#         if not self.active:
#             return False

#         if key == Qt.Key.Key_Up:
#             self.selected = max(0, self.selected - 1)
#             self._render()
#             return True
#         elif key == Qt.Key.Key_Down:
#             self.selected = min(len(self.options) - 1, self.selected + 1)
#             self._render()
#             return True
#         elif key == Qt.Key.Key_Return:
#             self._select_item()
#             return True
#         elif key == Qt.Key.Key_Escape:
#             self.remove()
#             return True

#     def deactivate(self):
#         """Деактивирует меню (оставляет видимым)"""
#         self.active = False
#         self._render()
#         if self.console.active_widgets == self:
#             self.console.active_widgets = None

#         cursor = self.console.textCursor()
#         cursor.setCharFormat(QTextCharFormat())
#         cursor.insertText(f"> ")

#     def remove(self):
#         """Полностью удаляет меню"""
#         self._clear()
#         if self.console.active_widgets == self:
#             self.console.active_widgets = None
#         self.console.show_prompt()

#     def _select_item(self):
#         self.remove()