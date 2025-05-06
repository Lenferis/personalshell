import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit
from PyQt6.QtGui import QTextCursor, QFont, QKeyEvent
from PyQt6.QtCore import Qt

from core.executor import CommandExecutor
from core.parser import CommandParser
from core.appcontext import AppContext, Session, Config
from core.register import CommandRegistry




class Console(QTextEdit):
    def __init__(self):
        super().__init__()
        self.prompt = "> "
        self.init_ui()

        self.appcontext = AppContext(Session('./session'), {}, self, {})
        self.parser = CommandParser()
        self.executor = CommandExecutor()
        self.register = CommandRegistry()
        self.register.register_from_config()

        self.executor.register_builtin_commands(self.register)

        print(self.register.command_classes, self.executor.commands)

    def init_ui(self):
        self.show_prompt()
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
        parse = self.parser.parse(command)
        result = self.executor.execute(parse, self.appcontext)

        # parse = self.parser(self.get_command())
        # result = self.executor(parse, self.appcontext)

        self.append(result)
        self.show_prompt()

    def get_command(self):
        return self.toPlainText().split(self.prompt)[-1].strip()

    def show_prompt(self):
        self.append(self.prompt)
        self.moveCursor(QTextCursor.MoveOperation.End)

