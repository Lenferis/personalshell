from src.modules.command import Command, ArgumentType
from typing import Any, Dict, List

class Echo(Command):
    """Command to print input text with environment variable substitution.
    
    Replaces ${ENV_VAR} patterns in input text with their current values
    from the session environment before outputting.
    """
    def __init__(self):
        super().__init__()
        self.name = "echo"
        self.description = "Print text with environment variable substitution"
        self.register_argument()
    def register_argument(self):
        """Register command arguments."""
        self.add_argument(
            name="text", 
            arg_type=ArgumentType.POSITIONAL, 
            required=False, 
            default="", 
            help="Text to print (supports ${ENV_VAR} substitution)"
        )
    def execute_main(self, parse, appcontext):
        """Execute echo command with environment variable substitution.
        Args:
            parse: Parsed command input containing:
                - 'parse': Parsed command structure
                - 'input_string': Original input text
            appcontext: Application context with session data
        Returns:
            Processed text with environment variables substituted
        """
        lentext = len(parse['parse'].get('command'))
        
        for env in appcontext.session.data["env"]:
            parse['input_string'] = parse['input_string'].replace(
                f'${{{env}}}', 
                appcontext.session.data['env'][env]
            )
            
        return parse['input_string'][lentext + 1:]