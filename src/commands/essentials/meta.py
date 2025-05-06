from commands.command import Command, ArgumentType
from datetime import datetime   

class VersionProgectCommand(Command):
    def __init__(self):
        super().__init__()
        self.name = "version"
        self.description = ""
        self.aliases = ["ver", "v"]
        self.subcommands = False
    
    def execute_main(self, parse, context):
        pass

class HelpCommand(Command):
    def __init__(self):
        super().__init__()
        self.name = "help"
        self.description: str = ""
        self.aliases = ["hp"]
        self.register_argument()
    def register_argument(self):
        self.add_argument(
            name="name",
            arg_type=ArgumentType.POSITIONAL,
            required=False,
            default=False,
            help="Help for a specific command"
        )
    def execute_main(self, parse, appcontext):
        
        return None
    
class DateCommand(Command):
    def __init__(self):
        super().__init__()
        self.name = "date"
        self.description: str = ""
    def execute_main(self, parse, appcontext):
        date = datetime.today()
        return date.strftime("%d/%m/%Y")
    
class TimeCommand(Command):
    def __init__(self):
        super().__init__()
        self.name = "time"
        self.description: str = ""
    def execute_main(self, parse, appcontext):
        now = datetime.now()
        return now.strftime("%H:%M:%S")
    
class DatetimeCommand(Command):
    def __init__(self):
        super().__init__()
        self.name = "datetime"
        self.description: str = ""
    def execute_main(self, parse, appcontext):
        now = datetime.now()
        return now.strftime("%d/%m/%Y %H:%M:%S")