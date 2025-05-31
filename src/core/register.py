import inspect
import importlib
from pathlib import Path

from src.modules.command import Command
from src.modules.plugin import Plugin
from src.core.appcontext import Config


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

    def register_plugin_from_module(self, path):
        """Регистрирует все команды из указанного модуля"""
        spec = importlib.util.spec_from_file_location("my_module", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and issubclass(obj, Command) and obj != Plugin:
                if obj().is_subcommand == False:
                    self.command_classes[obj().name] = obj
                    for alias in obj().aliases:
                        self.command_classes[alias] = obj

    
    def register_from_config(self):
        for module in Config().get_modulescore_path():
            self.register_from_module(module)
        for plugin in Config().get_modulesplugin_path():
            self.register_plugin_from_module(plugin)
    def get_all_commands(self):
        return self.command_classes
    