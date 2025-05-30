from component.plugin import Plugin


class HHH(Plugin):
    def __init__(self):
        super().__init__()
        self.name = "hhh"
        self.description: str = ""
    def execute_main(self, parse, appcontext):
        return "1ффффффффффффф"