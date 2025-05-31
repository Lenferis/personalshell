from src.modules.command import Command
from src.core.appcontext import Config
from typing import Any, Dict, List

class Plugin(Command):
    def __init__(self):
        super().__init__()
        self.config = Config()
    def validate_config(self) -> None:
        pass

