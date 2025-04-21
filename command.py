


class Command:
    def __init__(self):
        self.name = ""
        self.description = "No description provided"
        self.usage = ""
        self.aliases = []
    
    def validate(self, args, kwargs, flags):
        pass

    def execute(self, args, kwargs, flags, context):

        raise NotImplementedError("Command.execute() must be implemented")
        
    def help(self) -> str:

        return 0

