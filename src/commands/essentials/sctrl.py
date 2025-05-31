from src.modules.command import Command, ArgumentType
import sys

class ExitCommand(Command):
    """Command to exit the application."""
    
    def __init__(self):
        super().__init__()
        self.name = "exit"
        self.description = "Exit the application"
        self.aliases = ["quit", "logout"]
        self.register_argument()

    def execute_main(self, parse, context):
        """Terminate the application.
        
        Args:
            parse: Parsed command input
            context: Application context object
        """
        sys.exit()
        return None
    
class ClearCommand(Command):
    """Command to clear the console output."""
    
    def __init__(self):
        super().__init__()
        self.name = "clear"
        self.description = "Clear console output"
        self.aliases = ["cls"]
        self.register_argument()

    def execute_main(self, parse, appcontext):
        """Clear the console content.
        
        Args:
            parse: Parsed command input
            appcontext: Application context object
        """
        appcontext.console.clear()
        return None 
    
class HistoryCommand(Command):
    """Command to display command history."""
    
    def __init__(self):
        super().__init__()
        self.name = "history"
        self.description = "Show command history"
        self.register_argument()
        
    def register_argument(self):
        """Register command arguments."""
        self.add_argument(
            name="quantity",
            arg_type=ArgumentType.POSITIONAL,
            required=False,
            default=False,
            help="Number of commands to display (default: 10)"
        )
    
    def execute_main(self, parse, appcontext):
        """Retrieve and display command history.
        
        Args:
            parse: Parsed command input
            appcontext: Application context object
            
        Returns:
            Formatted command history or empty string
        """
        # Get quantity parameter or default to 10
        quantity = parse['parse']['args']['quantity'] if 'quantity' in parse['parse']['args'] else 10
        # Retrieve command history from session
        commands = appcontext.session.get_commands(quantity)
        return '\n'.join(commands)