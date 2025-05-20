from commands.command import Command, ArgumentType
import re, yaml

class ThemeCommand(Command):
    def __init__(self):
        super().__init__()
        self.name = "theme"
        self.description = ""
        self.aliases = ["th"]

        self.add_subcommand(ThemeSetCommand())
        self.add_subcommand(ThemeGetCommand())
    
    def execute_main(self, parse, appcontext):
        return '\n'.join(appcontext.console.thememanager.list_themes())
    
class ThemeSetCommand(Command):
    def __init__(self):
        super().__init__()
        self.name = "set"
        self.description = ""
        self.register_argument()
        self.is_subcommand = True
        

    def register_argument(self):
        self.add_argument(
            name="name",
            arg_type=ArgumentType.POSITIONAL,
            required=True,
            default=False,
            help="Theme name"
        )
        self.add_argument(
            name="default",
            arg_type=ArgumentType.FLAGS,
            required=False,
            default=False,
            help="Set theme as default(-d)"
        )

    def execute_main(self, parse, appcontext):
        themes = appcontext.console.thememanager.themes
        thememanager = appcontext.console.thememanager

        command = parse['input_string']
        # Извлекаем тему (включая дефисы) до первого флага
        match = re.match(r'^theme\s+set\s+(.+?)(?=\s+-|$)', command)
        # Ищем только валидные флаги (после пробела)
        flags = re.findall(r'\s+(-\w+)', command)
    
        if match:
            theme = match.group(1).strip()
            flags = [flag.replace('-',"") for flag in re.findall(r'\s+(-\w+)', command)]
        else:
            return "Invalid command format. Usage: {self.usage}"
        if theme in list(themes.keys()):
            thememanager.set_theme(theme)
            if 'd' in flags:
                appcontext.config.change_config(['user', 'theme', 'current'], theme)
            return f"Theme '{theme}' applied."
        else:
            return f"Theme '{theme}' not found. Available: {', '.join(appcontext.console.thememanager.themes.keys())}"

class ThemeGetCommand(Command):
    def __init__(self):
        super().__init__()
        self.name = "get"
        self.description = ""
        self.register_argument()
        self.is_subcommand = True

    def register_argument(self):
        self.add_argument(
            name="name",
            arg_type=ArgumentType.POSITIONAL,
            required=True,
            default=False,
            help="Theme name"
        )

    def execute_main(self, parse, appcontext):
        themes = appcontext.console.thememanager.themes
        thememanager = appcontext.console.thememanager

        commandtext = parse['input_string']
        match = re.match(r'^theme\s+get\s+(.+)$', commandtext, re.IGNORECASE)
        
        if match:
            theme_name = match.group(1).strip()
        else:
            return "Invalid command format. Usage: {self.usage}"
        if theme_name in list(themes.keys()):
            return yaml.dump(thememanager.get_theme(theme_name), sort_keys=False, allow_unicode=True)
        else:
            return f"Theme '{match}' not found. Available: {', '.join(themes.keys())}"