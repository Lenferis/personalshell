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
        self.kwargs = []
        self.flags = []
    
    def add_subcommand(self, command: 'Command'):
        self.subcommands[command.name] = command
        for alias in command.aliases:
            self.subcommands[alias] = command

    def add_argument(self, name, arg_type, required: bool = True, default: Any = False, help: str = "No description provided"):
        return self.argument.append(CommandArgument(name, arg_type, required, default, help))
    
    def register_argument():
        pass

    def validate(self, parse, context):
        pass
    def execute(self, parse, context):
        if parse['parse']['args'][0] in self.subcommands:
            return self.subcommands[parse['parse']['args'][0]].execute(parse['parse']['args'][1:],
                                                                       parse['parse']['kwargs'],
                                                                       parse['parse']['flags'],
                                                                       context)
        return self.execute_main(parse['parse']['args'], parse['parse']['kwargs'], parse['parse']['flags'], context)

    def execute_main(self, parse, context):

        raise NotImplementedError("Command.execute() must be implemented")
        
    def help(self) -> str:
        help_list = [
            f"Command: {self.name}",
            f"Description: {self.description}",
            f"Usage: {self.usage if self.usage else self.generate_usage()}",
            "Arguments:",
        ]
        for arg in self.argument:
            req = "" if arg.required == True else ""
            help_list.append(self.format_arg_name(arg))
        help_list.append(f"Aliases: {', '.join(self.aliases)}")
        return help_list
    def generate_usage(self):
        parts = [self.name]

        for arg in self.argument:
            if arg.arg_type == ArgumentType.POSITIONAL:
                parts.append(f"<{arg.name}>" if arg.required else f"[{arg.name}]")
            elif arg.arg_type == ArgumentType.NAMED:
                parts.append(f"--{arg.name}==VALUE" if arg.required else f"[--{arg.name}==VALUE]")
            elif arg.arg_type == ArgumentType.FLAGS:
                parts.append(f"-{arg.name}")
        return ' '.join(parts)

    def format_arg_name(self, arg: CommandArgument):
        if arg.arg_type == ArgumentType.NAMED:
            return f"--{arg}"
        elif arg.arg_type == ArgumentType.FLAGS:
            return f"-{arg}"
        return arg
    