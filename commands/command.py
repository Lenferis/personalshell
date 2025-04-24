from enum import Enum, auto
from typing import Any, Dict, List
from dataclasses import dataclass

class ArgumentType(Enum):
    POSITIONAL = auto()
    NAMED = auto()
    FLAGS = auto()

@dataclass
class CommandArgument:
    name: str
    arg_type: ArgumentType
    required: bool = False
    default: Any = False
    help: str = "No description provided"

class Command:
    """
    Command base class (template)
    """
    def __init__(self):
        self.name: str = ""
        self.description: str = "No description provided"
        self.usage: str = ""
        self.aliases: List[str] = []
        self.subcommands: Dict[str] = {
            'name': {},
            'aliases':{}
        }
        self.argument: List[str] = []
    
    def add_subcommand(self, command: 'Command') -> None:
        """
        Method to add a subcommand for the given command. Similar to registration with the command executor
        """
        self.subcommands['name'][command.name] = command
        for alias in command.aliases:
            self.subcommands['aliases'][alias] = command

    def add_argument(self, name: str, arg_type: ArgumentType, required: bool = True, default: Any = False, help: str = "No description provided") -> CommandArgument:
        """
        Adding an argument to the argument list. An argument is based on a data structure, the Argument class.
        They are divided into three types: positional, named and flags
        """
        return self.argument.append(CommandArgument(name, arg_type, required, default, help))
    
    def register_argument(self) -> None:
        """
        Function where in the future, in the class that inherited, will be the registration of all arguments.
        Called in __init__
        """
        pass

    def validate(self, parse: Dict[str, Any], context: Dict[str, Any]) -> Any:
        """
        This is where the validation for the team will be prescribed.
        For example, validation of arguments
        """
        pass
    def execute(self, parse: Dict[str, Any], context: Dict[str, Any]) -> Any:
        """
        The function of a command performer.
        It checks if there is a subcommand in the arguments and if there is, passes control to it, otherwise it performs its main function of the executor.
        """
        if parse['parse']['args'][0] in self.subcommands['name'].update(self.subcommands['alises']):
            return self.subcommands[parse['parse']['args'][0]].execute(parse, context)
        return self.execute_main(parse, context)

    def execute_main(self, parse: Dict[str, Any], context: Dict[str, Any]) -> Any:
        """
        The main function of the executor. The executor function transfers control to it if no other options are found
        """
        raise NotImplementedError("Command.execute() must be implemented")
        
    def help(self) -> Dict[str, Any]:
        """
        Function that creates a help(parameters) statement of the command
        """
        help_list = [
            f"Command: {self.name}",
            f"Description: {self.description}",
            f"Usage: {self.usage if self.usage else self.generate_usage()}",
            "Arguments:",
        ]
        for arg in self.argument:
            req = "(compulsory)" if arg.required == True else "(optional)"
            help_list.append(f"  {self.format_arg_name(arg)}    {arg.help} {req}")
        help_list.append(f"Aliases: {', '.join(self.aliases)}")

        help_list.append(f"Subcommand:")
        for scom in self.subcommands['name']:
            help_list.append(f"  {self.subcommands['name'][scom].name}    {self.subcommands['name'][scom].description}")
        
        return '\n'.join(help_list)
    def generate_usage(self) -> str:
        """
        Creates a usage string for the command, inserted into help
        """
        parts = [self.name]
        if self.subcommands:
            parts.append(f"(subcommands)")
        for arg in self.argument:
            if arg.arg_type == ArgumentType.POSITIONAL:
                parts.append(f"<{arg.name}>" if arg.required else f"[{arg.name}]")
            elif arg.arg_type == ArgumentType.NAMED:
                parts.append(f"--{arg.name}==VALUE" if arg.required else f"[--{arg.name}==VALUE]")
            elif arg.arg_type == ArgumentType.FLAGS:
                parts.append(f"-{arg.name}")
        return ' '.join(parts)

    def format_arg_name(self, arg: CommandArgument) -> str:
        """
        Formatting the argument view according to its view(positional = arg, named = --arg, flag = -arg)
        """
        if arg.arg_type == ArgumentType.NAMED:
            return f"--{arg.name}"
        elif arg.arg_type == ArgumentType.FLAGS:
            return f"-{arg.name}"
        
        return f"<{arg.name}>" if arg.required == True else f"[{arg.name}]"
    