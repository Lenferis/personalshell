import inspect
import importlib
from pathlib import Path

from commands.command import Command
from core.appcontext import Config


class CommandRegistry:
    def __init__(self):
        self.command_classes = {}

    def register_from_module(self, module_name: str):
        """Регистрирует все команды из указанного модуля"""
        module = importlib.import_module(module_name)
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and issubclass(obj, Command) and obj != Command:
                if obj().is_subcommand == False:
                    self.command_classes[obj().name] = obj
                    for alias in obj().aliases:
                        self.command_classes[alias] = obj
    
    def register_from_config(self):
        for module in Config().get_modulescore_path():
            self.register_from_module(module)

    # def register_from_directory(self, dir_path: str):
    #     """Автоматически регистрирует все команды из директории"""
    #     for file in Path(dir_path).glob('**/*.py'):
    #         module_path = f"commands.{Path(dir_path).name}.{file.name}"
    #         # self.register_from_module(module_path)
    #         print(module_path)

    def get_all_commands(self):
        return self.command_classes
    