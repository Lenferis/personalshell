import sys, re
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit
from PyQt6.QtGui import QTextCursor, QFont, QKeyEvent
from PyQt6.QtCore import Qt

from src.core.executor import CommandExecutor
from src.core.parser import CommandParser
from src.core.appcontext import AppContext, Session, Config
from src.core.register import CommandRegistry

from src.ui.theme import ThemeManager



class Console(QTextEdit):
    def __init__(self):
        super().__init__()
        self.config = Config()
        self.prompt = "> "

        self.thememanager = ThemeManager(self.config, self)
        self.init_ui()


        self.appcontext = AppContext(Session('./session'), self.config, self, {})

        self.parser = CommandParser()
        self.executor = CommandExecutor()
        self.register = CommandRegistry()
        self.register.register_from_config()
        self.executor.register_builtin_commands(self.register)

        self.widget = None

        self.object = {}

        

    def init_ui(self):
        self.show_prompt()
        self.thememanager.set_theme(Config().data['user']['theme']['current'])

    def keyPressEvent(self, event):
        if self.widget:
            if self.widget.handle_key(event):
                return
        else:
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
        self.appcontext.session.add_commands(command)
        parse = self.parser.parse(command)
        result = self.executor.execute(parse, self.appcontext)
        cursor = self.textCursor()
        if not self.widget:
            self.append(result)
            self.show_prompt()

    def get_command(self):
        return re.match(r'>(.*)', self.toPlainText().split("\n")[-1]).group(1)

    def show_prompt(self):
        self.append(self.prompt)
        self.moveCursor(QTextCursor.MoveOperation.End)

# import sys
# from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit
# from PyQt6.QtGui import QTextCursor, QFont, QKeyEvent
# from PyQt6.QtCore import Qt

# from core.executor import CommandExecutor
# from core.parser import CommandParser
# from core.appcontext import AppContext, Session, Config
# from core.register import CommandRegistry

# from ui.theme import ThemeManager



# # class Console(QTextEdit):
# #     def __init__(self):
# #         super().__init__()
# #         self.config = Config()
# #         self.prompt = "> "

# #         self.thememanager = ThemeManager(self.config, self)
# #         self.init_ui()


# #         self.appcontext = AppContext(Session('./session'), self.config, self, {})

# #         self.parser = CommandParser()
# #         self.executor = CommandExecutor()
# #         self.register = CommandRegistry()
# #         self.register.register_from_config()
# #         self.executor.register_builtin_commands(self.register)

        

# #     def init_ui(self):
# #         self.show_prompt()
# #         self.thememanager.set_theme(Config().data['user']['theme']['current'])

# #     def keyPressEvent(self, event):
# #         if event.key() == Qt.Key.Key_Return:
# #             self.process_command()
# #         elif event.key() == Qt.Key.Key_Backspace:
# #             self.handle_backspace()
# #         else:
# #             if self.textCursor().position() == self.document().characterCount() - 1:
# #                 super().keyPressEvent(event)

# #     def handle_backspace(self):

# #         def is_cursor_at_end(self) -> bool:
# #             return self.textCursor().position() == self.document().characterCount() - 1 
        
# #         if is_cursor_at_end(self) and self.textCursor().positionInBlock() > len(self.prompt):
                
# #                 super().keyPressEvent(QKeyEvent(QKeyEvent.Type.KeyPress, Qt.Key.Key_Backspace, Qt.KeyboardModifier.NoModifier))

# #     def get_prompt_pos(self):

# #         return len(self.toPlainText()) - len(self.prompt)

# #     def process_command(self):
# #         command = self.get_command()
# #         self.appcontext.session.add_commands(command)
# #         parse = self.parser.parse(command)
# #         result = self.executor.execute(parse, self.appcontext)
# #         cursor = self.textCursor()
# #         cursor.setPosition(5)
# #         # parse = self.parser(self.get_command())
# #         # result = self.executor(parse, self.appcontext)
# #         if result != 'app':
# #             self.append(result)
# #         self.show_prompt()

# #     def get_command(self):
# #         return self.toPlainText().split(self.prompt)[-1].strip()

# #     def show_prompt(self):
# #         self.append(self.prompt)
# #         self.moveCursor(QTextCursor.MoveOperation.End)

