from component.command import Command, ArgumentType

class EnvCommand(Command):
    def __init__(self):
        super().__init__()
        self.name = "env"
        self.description = ""
        
        self.add_subcommand(EnvSetCommand())
        self.add_subcommand(EnvUnsetCommand())
    
    def execute_main(self, parse, appcontext):
        envlist = []
        for env in appcontext.session.data['env']:
            envlist.append(f"{env}: {appcontext.session.data['env'][env]}")
        return '\n'.join(envlist)
    
class EnvSetCommand(Command):
    def __init__(self):
        super().__init__()
        self.name = "set"
        self.description = ""
        self.register_argument()
        self.is_subcommand = True

    def register_argument(self):
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
        key = parse['parse']['args'][0]
        value = parse['parse']['args'][1]
        appcontext.session.add_env(key, value)
        return str(parse['parse']['args'])

class EnvUnsetCommand(Command):
    def __init__(self):
        super().__init__()
        self.name = "unset"
        self.description = ""
        self.register_argument()
        self.is_subcommand = True

    def register_argument(self):
        self.add_argument(
            name="key",
            arg_type=ArgumentType.POSITIONAL,
            required=True,
            default=False,
            help="Key name"
        )    
    def execute_main(self, parse, appcontext):
        key = parse['parse']['args'][0]

        if key in appcontext.session.data['env']:
            del appcontext.session.data['env'][key]

        return ""