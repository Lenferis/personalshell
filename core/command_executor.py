from .session import Session
from .history_manager import HistoryManager
from typing import Any, Dict

class CommandExecutor:
    """
    Class of command executor
    """
    def __init__(self):
        self.commands = {}
        self.commands_aliases = []
        self.context = Session('./session').load()
        self.logger = HistoryManager('./logs')
    def register(self, Command: object) -> None:
        """
        Registration of the command in the executor for further detection in the request and execution
        """
        self.commands[Command.name] = Command
        for alias in Command.aliases:
            self.commands[alias] = Command
    def execute(self, parse: Dict[str, Any]) -> Any: #[ec]
        """
        A function that accesses a command class and its executor functions. Basic function for project operation
        """
        print(self.context)
        if parse['parse']['command'] not in self.commands:
            return f"The command {parse['parse']['command']} doesn't exist."

        result = self.commands[parse['parse']['command']].execute(parse, self.context)
        self.logger.log_command_brief(parse['parse']['command'])
        return result


        

