import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit
from PyQt6.QtGui import QTextCursor, QFont, QKeyEvent
from PyQt6.QtCore import Qt

class Console(QTextEdit):
    def __init__(self):
        super().__init__()
        self.prompt = "> "
        self.init_ui()
        self.show_prompt()

    def init_ui(self):
        self.setStyleSheet("background: black; color: white;")
        self.setFont(QFont("Courier New", 11))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return:
            self.process_command()
        elif event.key() == Qt.Key.Key_Backspace:
            self.handle_backspace()
        else:
            if self.textCursor().position() == self.document().characterCount() - 1:
                super().keyPressEvent(event)

    def handle_backspace(self):

        def is_cursor_at_end(self) -> bool:
            return self.textCursor().position() == self.document().characterCount() - 1 
        
        if is_cursor_at_end(self) and self.textCursor().positionInBlock() > len(self.prompt):
                
                super().keyPressEvent(QKeyEvent(QKeyEvent.Type.KeyPress, Qt.Key.Key_Backspace, Qt.KeyboardModifier.NoModifier))

    def get_prompt_pos(self):

        return len(self.toPlainText()) - len(self.prompt)

    def process_command(self):
        command = self.get_command()
        result = self.execute(command)
        self.append(result)
        self.show_prompt()

    def get_command(self):
        return self.toPlainText().split(self.prompt)[-1].strip()

    def execute(self, cmd):
        if cmd == "clear":
            self.clear()
            return ""
        elif cmd == "exit":
            sys.exit()
        return f"Unknown command: {cmd}"

    def show_prompt(self):
        self.append(self.prompt)
        self.moveCursor(QTextCursor.MoveOperation.End)

