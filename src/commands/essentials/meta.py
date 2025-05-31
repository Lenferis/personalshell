from src.modules.command import Command, ArgumentType
from datetime import datetime

class VersionProgectCommand(Command):
    """Command to display the current application version."""
    def __init__(self):
        super().__init__()
        self.name = "version"
        self.description = "Display the current application version"
        self.aliases = ["ver", "v"]
        self.subcommands = False
    def execute_main(self, parse, appcontext):
        """Retrieve and return version information from configuration.
        Args:
            parse: Parsed command input
            appcontext: Application context object
        Returns:
            Version string from application configuration
        """
        return appcontext.config.get_version()

class HelpCommand(Command):
    """Command to display help information about available commands."""
    
    def __init__(self):
        super().__init__()
        self.name = "help"
        self.description = "Display help information for commands"
        self.aliases = ["hp"]
        self.register_argument()
        
    def register_argument(self):
        """Register optional argument for command-specific help."""
        self.add_argument(
            name="command",
            arg_type=ArgumentType.POSITIONAL,
            required=False,
            default=False,
            help="Get detailed help for a specific command"
        )
        
    def execute_main(self, parse, appcontext):
        """Execute help command logic (implementation pending).
        Args:
            parse: Parsed command input
            appcontext: Application context object
        Returns:
            Help information string (to be implemented)
        """
        # Placeholder for actual help implementation
        return "Help system - under development"

class DateCommand(Command):
    """Command to display the current date."""
    def __init__(self):
        super().__init__()
        self.name = "date"
        self.description = "Display the current date"
    def execute_main(self, parse, appcontext):
        """Get and format current date.
        Args:
            parse: Parsed command input
            appcontext: Application context object
        Returns:
            Current date in DD/MM/YYYY format
        """
        date = datetime.today()
        return date.strftime("%d/%m/%Y")
    
class TimeCommand(Command):
    """Command to display the current time."""
    def __init__(self):
        super().__init__()
        self.name = "time"
        self.description = "Display the current time"
    def execute_main(self, parse, appcontext):
        """Get and format current time.
        Args:
            parse: Parsed command input
            appcontext: Application context object
        Returns:
            Current time in HH:MM:SS format
        """
        now = datetime.now()
        return now.strftime("%H:%M:%S")
    
class DatetimeCommand(Command):
    """Command to display the current date and time."""
    def __init__(self):
        super().__init__()
        self.name = "datetime"
        self.description = "Display the current date and time"
    def execute_main(self, parse, appcontext):
        """Get and format combined date and time.
        Args:
            parse: Parsed command input
            appcontext: Application context object
        Returns:
            Current datetime in DD/MM/YYYY HH:MM:SS format
        """
        now = datetime.now()
        return now.strftime("%d/%m/%Y %H:%M:%S")