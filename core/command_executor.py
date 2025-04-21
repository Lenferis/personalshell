class CommandExecutor:
    def __init__(self):
        self.commands = {}
        self.commands_aliases = {}
    
    def register(self, Command):
        self.commands[Command.name] = Command
        for alias in Command.aliases:
            self.commands_aliases[alias] = Command

    def execute(self, name, args, kwargs, flags, context):
        if name not in self.commands_aliases:
            return 0
        command = self.commands[name]
        return command.execute()
