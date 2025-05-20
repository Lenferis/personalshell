from commands.command import Command, ArgumentType
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