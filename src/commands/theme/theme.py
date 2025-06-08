from src.modules.command import Command, ArgumentType
from src.modules.widgets.widget import Widget
import re, yaml
from PyQt6.QtGui import QTextCursor
from PyQt6.QtCore import Qt

class ThemeCommand(Command):
    """Command to manage console color themes."""
    def __init__(self):
        super().__init__()
        self.name = "theme"
        self.description = "Manage console color themes"
        self.aliases = ["th"]

        self.add_subcommand(ThemeSetCommand())
        self.add_subcommand(ThemeGetCommand())
    
    def execute_main(self, parse, appcontext):
        """List available themes when no subcommand is specified.
        Args:
            parse: Parsed command input
            appcontext: Application context object
        Returns:
            Newline-separated list of theme names
        """
        return '\n'.join(appcontext.console.thememanager.list_themes())

class ThemeListWidget(Widget):
    """Interactive searchable list widget for theme selection."""
    def __init__(self, console, config, thememanager, themes):
        """
        Args:
            console: Console reference
            config: Application configuration
            thememanager: Theme management instance
            themes: List of available theme names
        """
        stop_method = "remove"
        super().__init__(console)
        self.config = config
        self.thememanager = thememanager
        self.start_theme = self.thememanager.current_theme.data['meta']['name']

        self.items = themes
        self.filtered_items = themes

        self.selected_index = self.items.index(self.start_theme)
        self.items_per_page = 10
        self.page = self.selected_index // self.items_per_page

        self.query = ""
        self.active = True

        self.formats = {
            'query': self._create_format("#00D9FF"),
            'normal': self._create_format("#00FF00"),
            'selected': self._create_format("#FFFFFF", "#004400"),
            'inactive': self._create_format("#888888")
        }
    
    def _render(self):
        """Render the search interface and theme list with pagination."""
        self._clear()
        cursor = self.console.textCursor()
        cursor.setPosition(self.get_start_pos())

        cursor.insertText(f"Search: {self.query}_\n", self.formats['query'])
        start = self.page * self.items_per_page
        end = start + self.items_per_page
        for i, item in enumerate(self.filtered_items[start:end]):
            global_index = start + i
            cursor.insertText(f"{'>' if global_index == self.selected_index else ''} {item}\n", 
                             self.formats['selected'] if global_index == self.selected_index else self.formats['normal'] )

        total_pages = max(1, (len(self.filtered_items) - 1) // self.items_per_page + 1)
        cursor.insertText(f"{self.page + 1} / {total_pages}", self._create_format("gray"))

        cursor.insertText("\n↑/↓ select, ←/→ page select, Enter use, D use default, Esc close\n", 
                         self._create_format("gray"))
        self.console.setTextCursor(cursor)

    def view_theme(self, select):
        """Preview selected theme without permanent application.
        Args:
            select: Index of selected theme in filtered list
        """
        theme = self.filtered_items[select]
        self.thememanager.set_theme(theme)

    def use_theme(self, select):
        """Apply selected theme and close widget.
        Args:
            select: Index of selected theme in filtered list
        """
        theme = self.filtered_items[select]
        self.thememanager.set_theme(theme)
        self.stop()
        
    def change_default_theme(self, select):
        """Set selected theme as default and close widget.
        Args:
            select: Index of selected theme in filtered list
        """
        theme = self.filtered_items[select]
        self.thememanager.set_theme(theme)
        self.config.change_config(['user', 'theme', 'current'], theme)
        self.stop()

    def handle_key(self, event):
        """Handle keyboard input for search and navigation.
        Args:
            event: Qt key event
        Returns:
            True if key was handled, False otherwise
        """
        if not self.active:
            return False
        
        key = event.key()
        text = event.text()

        if key == Qt.Key.Key_Escape:
            self.thememanager.set_theme(self.start_theme)
            self.stop()
            return True
        elif key == Qt.Key.Key_Backspace:
            self.query = self.query[:-1]
            self._filter()
        elif key == Qt.Key.Key_Return:
            self.use_theme(self.selected_index)
            return True
        elif key == Qt.Key.Key_Left:
            self.page = max(0, self.page - 1)
            self.selected_index = self.page * self.items_per_page
            self.view_theme(self.selected_index)
        elif key == Qt.Key.Key_Right:
            max_page = max(0, (len(self.filtered_items) - 1) // self.items_per_page)
            self.page = min(max_page, self.page + 1)
            self.selected_index = self.page * self.items_per_page
            self.view_theme(self.selected_index)
        elif key == Qt.Key.Key_Up:
            self.selected_index = max(0, self.selected_index - 1)
            self.view_theme(self.selected_index)
        elif key == Qt.Key.Key_Down:
            self.selected_index = min(len(self.filtered_items) - 1, self.selected_index + 1)
            self.view_theme(self.selected_index)
            self.page = self.selected_index // self.items_per_page
        elif key == Qt.Key.Key_Control:
            self.change_default_theme(self.selected_index)
            return True
        else:
            self.query += text
            self._filter()
        self._render()
        return True

    def _filter(self):
        """Filter theme list based on current search query."""
        self.filtered_items = [item for item in self.items if self.query.lower() in item.lower()]
        self.page = 0
        self.selected_index = 0
        if not self.filtered_items:
            self.filtered_items = ["(no themes found)"]

class ThemeSetCommand(Command):
    """Subcommand for applying themes with optional default setting."""
    def __init__(self):
        super().__init__()
        self.name = "set"
        self.description = "Apply a theme to the console"
        self.register_argument()
        self.is_subcommand = True

    def register_argument(self):
        """Register command arguments."""
        self.add_argument(
            name="name",
            arg_type=ArgumentType.POSITIONAL,
            required=False,
            default=False,
            help="Theme name to apply"
        )
        self.add_argument(
            name="default",
            arg_type=ArgumentType.FLAGS,
            required=False,
            default=False,
            help="Set theme as default (-d)"
        )

    def execute_main(self, parse, appcontext):
        """Execute theme setting logic.
        Args:
            parse: Parsed command input
            appcontext: Application context object
        Returns:
            Status message or interactive widget
        """
        themes = appcontext.console.thememanager.themes
        thememanager = appcontext.console.thememanager
        
        # Interactive mode if no theme specified
        if not parse['parse']['args']:
            themelist = ThemeListWidget(
                appcontext.console, 
                appcontext.config, 
                thememanager, 
                list(themes.keys()))
            appcontext.console.widget = themelist
            themelist.show()
            return ""
        
        # Parse theme name and flags from command
        command = parse['input_string']
        match = re.match(r'^theme\s+set\s+(.+?)(?=\s+-|$)', command)
        flags = re.findall(r'\s+(-\w+)', command)
    
        if match:
            theme = match.group(1).strip()
            flags = [flag.replace('-',"") for flag in flags]
        else:
            return f"Invalid command format. Usage: {self.usage}"
        
        # Apply theme
        if theme in themes:
            thememanager.set_theme(theme)
            if 'd' in flags:
                appcontext.config.change_config(['user', 'theme', 'current'], theme)
            return f"Theme '{theme}' applied."
        else:
            return f"Theme '{theme}' not found. Available themes: {', '.join(themes.keys())}"

class ThemeGetCommand(Command):
    """Subcommand for viewing theme configuration details."""
    def __init__(self):
        super().__init__()
        self.name = "get"
        self.description = "View theme configuration details"
        self.register_argument()
        self.is_subcommand = True

    def register_argument(self):
        """Register command arguments."""
        self.add_argument(
            name="name",
            arg_type=ArgumentType.POSITIONAL,
            required=True,
            default=False,
            help="Theme name to inspect"
        )

    def execute_main(self, parse, appcontext):
        """Retrieve and display theme configuration.
        Args:
            parse: Parsed command input
            appcontext: Application context object
        Returns:
            YAML-formatted theme configuration or error message
        """
        themes = appcontext.console.thememanager.themes
        thememanager = appcontext.console.thememanager

        commandtext = parse['input_string']
        match = re.match(r'^theme\s+get\s+(.+)$', commandtext, re.IGNORECASE)
        
        if match:
            theme_name = match.group(1).strip()
        else:
            return f"Invalid command format. Usage: {self.usage}"
        
        if theme_name in themes:
            return yaml.dump(
                thememanager.get_theme(theme_name), 
                sort_keys=False, 
                allow_unicode=True
            )
        else:
            return f"Theme '{theme_name}' not found. Available themes: {', '.join(themes.keys())}"