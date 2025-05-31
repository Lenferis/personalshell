from src.modules.command import Command, ArgumentType

class EnvCommand(Command):
    """Main environment variable management command.
    
    This command handles viewing, setting, and unsetting environment variables 
    within the current session. When executed without subcommands, it displays 
    all current environment variables in KEY: VALUE format.
    """
    
    def __init__(self):
        super().__init__()
        self.name = "env"
        self.description = "Manage session environment variables"
        
        self.add_subcommand(EnvSetCommand())
        self.add_subcommand(EnvUnsetCommand())
    
    def execute_main(self, parse, appcontext):
        """Display all current environment variables.
        
        Args:
            parse: Parsed command input
            appcontext: Application context object
            
        Returns:
            Formatted string of environment variables (KEY: VALUE)
        """
        envlist = []
        for env in appcontext.session.data['env']:
            envlist.append(f"{env}: {appcontext.session.data['env'][env]}")
        return '\n'.join(envlist)
    
class EnvSetCommand(Command):
    """Subcommand to set environment variables."""
    
    def __init__(self):
        super().__init__()
        self.name = "set"
        self.description = "Set an environment variable"
        self.register_argument()
        self.is_subcommand = True

    def register_argument(self):
        """Register required arguments for setting variables.
        
        Arguments:
            key: Environment variable name
            value: Value to assign to the variable
        """
        self.add_argument(
            name="key",
            arg_type=ArgumentType.POSITIONAL,
            required=True,
            default=False,
            help="Key name"
        )
        self.add_argument(
            name="value",
            arg_type=ArgumentType.POSITIONAL,
            required=True,
            default=False,
            help="Value"
        )
        
    def execute_main(self, parse, appcontext):
        """Set a new environment variable in session.
        
        Args:
            parse: Parsed command input containing arguments
            appcontext: Application context object
            
        Returns:
            Confirmation string with the set key-value pair
        """
        key = parse['parse']['args'][0]
        value = parse['parse']['args'][1]
        appcontext.session.add_env(key, value)
        return f"Set {key} = {value}"

class EnvUnsetCommand(Command):
    """Subcommand to unset (remove) environment variables."""
    
    def __init__(self):
        super().__init__()
        self.name = "unset"
        self.description = "Remove an environment variable"
        self.register_argument()
        self.is_subcommand = True

    def register_argument(self):
        """Register required arguments for unsetting variables.
        
        Arguments:
            key: Environment variable name to remove
        """
        self.add_argument(
            name="key",
            arg_type=ArgumentType.POSITIONAL,
            required=True,
            default=False,
            help="Key name"
        )    
        
    def execute_main(self, parse, appcontext):
        """Remove an environment variable from session.
        
        Args:
            parse: Parsed command input containing arguments
            appcontext: Application context object
            
        Returns:
            Empty string (no confirmation message needed)
        """
        key = parse['parse']['args'][0]
        if key in appcontext.session.data['env']:
            del appcontext.session.data['env'][key]
        return ""