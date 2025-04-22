from .session import Session


class CommandExecutor:
    def __init__(self):
        self.commands = {}
        self.commands_aliases = {}
        self.context = Session.load()
    
    def register(self, Command):
        self.commands[Command.name] = {
            "command": Command,
            "aliases": Command.aliases
        }
    def execute(self, parse):
        if parse['parse']['name'] not in self.commands_aliases:
            return f"The command {parse['parse']['name']} doesn't exist."
        command = self.commands[parse['parse']['name']]
        return command.execute(parse, self.context)
        # try:
        #     if name not in self.commands_aliases:
        #         return f"The command {name} doesn't exist."
            
        #     result = self.commands[name].execute()
        #     self.logger(name, args, kwargs, flags, context, True, result)
        #     return result
        # except Exception as e:
        #     self.error_logger(name, args, kwargs, flags, context, False, result)

