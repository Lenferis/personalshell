from typing import Any, Dict

class CommandExecutor:
    """
    Class of command executor
    """
    def __init__(self):
        self.commands = {}
        self.commands_aliases = []
        # Передать сессию в класс консоли 
    
    def register_builtin_commands(self, register):
        """"""
        for cmd_name, cmd_class in register.get_all_commands().items():
            self.register(cmd_class())

    def register(self, Command: object) -> None:
        """
        Registration of the command in the executor for further detection in the request and execution
        """
        self.commands[Command.name] = Command
        for alias in Command.aliases:
            self.commands[alias] = Command
    def execute(self, parse: Dict[str, Any], appcontext) -> Any: #[ec]
        """
        A function that accesses a command class and its executor functions. Basic function for project operation
        """
        if parse['parse']['command'] not in self.commands:
            return f"The command {parse['parse']['command']} doesn't exist."

        result = self.commands[parse['parse']['command']].execute(parse, appcontext)
        return result
    



        

