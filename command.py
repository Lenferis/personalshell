from enum import Enum, auto
from typing import Any

class ArgumentType(Enum):
    POSITIONAL = auto()
    NAMED = auto()
    FLAGS = auto()

class CommandArgument:
    name: str
    arg_type: ArgumentType
    required: bool = False
    default: Any = False
    help: str = "No description provided"




class Command:
    def __init__(self):
        self.name = ""
        self.description = "No description provided"
        self.usage = ""
        self.aliases = []
        self.subcommands = {}
        self.argument = []
    
    def add_subcommand(self, command: 'Command'):
        self.subcommands[command.name] = command
        for alias in command.aliases:
            self.subcommands[alias] = command

    def add_argument(self, name, arg_type, required: bool = True, default: Any = False, help: str = "No description provided"):
        return self.argument.append(CommandArgument(name, arg_type, required, default, help))
    
    def register_argument():
        pass

    def validate(self, args, kwargs, flags):
        pass
    def execute(self, args, kwargs, flags, context):
        if args[0] in self.subcommands:
            return self.subcommands[args[0]].execute(args[1:], kwargs, flags, context)
        return self.execute_main(args, kwargs, flags, context)

    def execute_main(self, args, kwargs, flags, context):

        raise NotImplementedError("Command.execute() must be implemented")
        
    def help(self) -> str:
        help_list = [
            f"Command: {self.name}",
            f"Description: {self.description}",
            f"Usage: {self.usage}",
            "Arguments:",
        ]
        for arg in self.argument:
            req = "" if arg.required == True else ""
            help_list.append(self.format_arg_name(arg))
        help_list.append(f"Aliases: {', '.join(self.aliases)}")
        return help_list

    def format_arg_name(self, arg: CommandArgument):
        if arg.arg_type == ArgumentType.NAMED:
            return f"--{arg}"
        elif arg.arg_type == ArgumentType.FLAGS:
            return f"-{arg}"
        return arg
    