class CommandExecutor:
    def __init__(self):
        self.commands = {}
        self.commands_aliases = {}
    
    def register(self, Command):
        self.commands[Command.name] = {
            "command": Command,
            "aliases": Command.aliases
        }
    def execute(self, name, args, kwargs, flags, context):
        if name not in self.commands_aliases:
            return 0
        command = self.commands[name]
        return command.execute()
