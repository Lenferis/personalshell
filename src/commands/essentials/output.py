from commands.command import Command, ArgumentType
from typing import Any, Dict, List

class Echo(Command):
    def __init__(self):
        super().__init__()
        self.name = "echo"
        self.description = ""
        self.aliases = [""]
        self.register_argument()

    def register_argument(self):
        self.add_argument(name="add", arg_type = ArgumentType.POSITIONAL, required = False, default = False, help = "wrerwwre")
    
    def execute_main(self, parse, appcontext):
        lentext = len(parse['parse'].get('command'))
        for env in appcontext.session.data["env"]:
            parse['input_string'] = parse['input_string'].replace(f'${{{env}}}', appcontext.session.data['env'][env])
        return parse['input_string'][lentext + 1:]

