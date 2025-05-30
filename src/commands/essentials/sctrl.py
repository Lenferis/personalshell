from modules.command import Command, ArgumentType
import sys

class ExitCommand(Command):
    def __init__(self):
        super().__init__()
        self.name = "exit"
        self.description: str = ""
        self.aliases = ["quit", "logout"]
        self.register_argument()

    def execute_main(self, parse, context):
        sys.exit()
        return None
    
class ClearCommand(Command):
    def __init__(self):
        super().__init__()
        self.name = "clear"
        self.description: str = ""
        self.aliases = ["cls"]
        self.register_argument()

    def execute_main(self, parse, appcontext):
        appcontext.console.clear()
        return None 
    
class HistoryCommand(Command):
    def __init__(self):
        super().__init__()
        self.name = "history"
        self.description: str = ""
        self.register_argument()
    def register_argument(self):
        self.add_argument(
            name="quantity",
            arg_type=ArgumentType.POSITIONAL,
            required=False,
            default=False,
            help="Number of commands to show"
        )
    def execute_main(self, parse, appcontext):
        quantity = parse['parse']['args']['quantity'] if 'quantity' in parse['parse']['args'] else 10
        command = appcontext.session.get_commands(quantity)
        return '\n'.join(command)
    

from PyQt6.QtWidgets import QTextEdit, QApplication
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QTextCursor, QKeyEvent, QMouseEvent

class IterateCommand:
    """
    Класс для команды перебора списка с обновлением строки без удаления prompt.
    """
    def __init__(self, console, items, interval=500):
        self.console = console
        self.items = items
        self.interval = interval
        self.index = 0
        self.start_block = None
        self.timer = QTimer()
        self.timer.timeout.connect(self._update)

    def start(self):
        # Блокируем ввод во время выполнения
        self.console.setReadOnly(True)

        # Найти позицию для первого элемента (следом за prompt)
        self.console.append(f"Iterating: {self.items[0]}")
        self.start_block = self.console.document().blockCount() - 1
        self.console.moveCursor(QTextCursor.MoveOperation.End)
        self.timer.start(self.interval)

    def _update(self):
        self.index += 1
        if self.index < 10:
            block = self.console.document().findBlockByNumber(self.start_block)
            cursor = self.console.textCursor()
            cursor.setPosition(block.position())
            cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock, QTextCursor.MoveMode.KeepAnchor)
            cursor.removeSelectedText()
            cursor.insertText(f"Iterating: {"#"*self.index}")
            self.console.moveCursor(QTextCursor.MoveOperation.End)
        else:
            self.timer.stop()
            # Разблокировать ввод и показать новый prompt
            self.console.setReadOnly(False)



from PyQt6.QtGui import QTextCursor, QMouseEvent, QColor, QTextCharFormat, QKeyEvent
from PyQt6.QtCore import Qt

class DropdownMen:
    def __init__(self, console, options: list):
        self.console = console
        self.options = options
        self.selected = 0
        self.visible = False
        self.saved_text = ""
        self.saved_cursor_pos = 0
        
        self.formats = {
            'normal': self.create_format("#00FF00"),
            'selected': self.create_format("#FFFFFF", "#004400")
        }

    def create_format(self, fg, bg=None):
        fmt = QTextCharFormat()
        fmt.setForeground(QColor(fg))
        if bg:
            fmt.setBackground(QColor(bg))
        return fmt

    def show(self):
        if self.visible:
            return
        self.visible = True
        self.saved_text = self.console.toPlainText()
        self.saved_cursor_pos = self.console.textCursor().position()
        self._render()

    def hide(self):
        if not self.visible:
            return
        self.visible = False
        self.console.setPlainText(self.saved_text)
        cursor = self.console.textCursor()
        cursor.setPosition(self.saved_cursor_pos)
        self.console.setTextCursor(cursor)

    def handle_key(self, key: int) -> bool:
        if not self.visible:
            return False

        if key == Qt.Key.Key_Up:
            self.selected = max(0, self.selected - 1)
            self._render()
            return True
        elif key == Qt.Key.Key_Down:
            self.selected = min(len(self.options)-1, self.selected + 1)
            self._render()
            return True
        elif key == Qt.Key.Key_Return:
            self._select_item()
            return True
        elif key == Qt.Key.Key_Escape:
            self.hide()
            return True
            
        return False

    def _render(self):
        self.console.setPlainText("")
        cursor = self.console.textCursor()
        for i, option in enumerate(self.options):
            fmt = self.formats['selected'] if i == self.selected else self.formats['normal']
            cursor.insertText(f"{'> ' if i == self.selected else '  '}{option}\n", fmt)
        self.console.setTextCursor(cursor)

    def _select_item(self):
        selected = self.options[self.selected]
        self.console.append(f"\nSelected: {selected}\n> ")
        self.hide()

class DropdownMenu:
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


class SettingCommand(Command):
    def __init__(self):
        super().__init__()
        self.name = "s"
        self.description = ""

    
    def execute_main(self, parse, appcontext):
        menu = DropdownMenu(appcontext.console, ["Звук", "Музыка", "Графика", "Субтитры"])
        appcontext.console.widget = menu
        menu.show()
