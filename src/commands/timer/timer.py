from src.modules.command import Command, ArgumentType
from src.modules.widgets.widget import Widget
from PyQt6.QtGui import QTextCursor, QKeyEvent
from PyQt6.QtCore import Qt, QTimer

class TimerWidget(Widget):
    """Interactive widget for creating and managing countdown timers."""
    
    def __init__(self, console):
        """
        Initialize timer widget with default state and configurations.
        
        Args:
            console: Reference to console object for interaction
        """
        super().__init__(console)
        # Widget states: 'menu_input', 'timer_list', 'input', 'running', 'paused'
        self.state = 'menu_input'
        self.time_left = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self._tick)
        self.timer_input = "hh:mm:ss"
        self.active = True
        self.name_timer = fr"#{0 if 'timer' not in self.console.object else len(self.console.object['timer'])}"
        
        self.selected_timer = 0
        # Text formatting for different widget states
        self.formats = {
            'menu_input': self._create_format("#00F2FF", "#525554"),
            'timer_list': self._create_format("#7CFE4C", "#D8D8D8"),
            'timer_list selected': self._create_format("#F2F7F0", "#3BFB00"),
            'input': self._create_format("#FFFFFF", "#333333"),
            'running': self._create_format("#000000", "#00FF00"),
            'paused': self._create_format("#000000", "#FFFF00")
        }
    
    def _render(self):
        """Render the timer interface based on current state."""
        self._clear()
        cursor = self.console.textCursor()
        cursor.setPosition(self.get_start_pos())
        
        if self.state == 'menu_input':
            cursor.insertText(f"Timers\n", self.formats['menu_input'])
            cursor.insertText(f"Enter a name for the timer: {self.name_timer}_\n", self.formats['menu_input'])
            cursor.insertText("[Enter] Create a new timer [L] List timers [Esc] Cancel", self.formats['menu_input'])
        
        elif self.state == 'timer_list':
            if 'timer' in self.console.object:
                for count, timer in enumerate(self.console.object['timer'].values()):
                    name = timer.name_timer
                    hours = timer.time_left // 3600
                    mins = (timer.time_left % 3600) // 60
                    secs = (((timer.time_left % 3600) % 60) % 60)
                    if count == self.selected_timer:
                        cursor.insertText(f"{name} - {hours}:{mins}:{secs}\n", self.formats['timer_list selected'])
                    else:
                        cursor.insertText(f"{name} - {hours}:{mins}:{secs}\n", self.formats['input'])
            else:
                cursor.insertText(f"There are no active timers\n", self.formats['input'])
            cursor.insertText("[Enter] Select timer [Esc] Cancel", self.formats['input'])
                
        elif self.state == 'input':
            cursor.insertText(f"Timer {self.name_timer}\n", self.formats['input'])
            cursor.insertText(f"Set Timer (hh:mm:ss): {self.timer_input}\n", self.formats['input'])
            cursor.insertText("[Enter] Start  [Esc] Cancel\n", self.formats['input'])
        
        elif self.state in ('running', 'paused'):
            hours = self.time_left // 3600
            mins = (self.time_left % 3600) // 60
            secs = (((self.time_left % 3600) % 60) % 60)
            fmt = self.formats['running'] if self.state == 'running' else self.formats['paused']
            cursor.insertText(f"Timer {self.name_timer}: {hours}:{mins}:{secs}\n", fmt)
            cursor.insertText("[Space] Pause/Resume  [R] Reset  [Alt] Swipe the timer  [Esc] Exit", fmt)
        
        self.console.setTextCursor(cursor)

    def handle_key(self, event):
        """Handle keyboard input for timer management.
        
        Args:
            event: Qt key event object
            
        Returns:
            True if key was handled, False otherwise
        """
        if not self.active:
            return False
        
        key = event.key()
        text = event.text()

        # Main menu state handling
        if self.state == 'menu_input':
            if key == Qt.Key.Key_Return:
                self.state = "input"
                self._render()
                return True
            if key == Qt.Key.Key_Backspace:
                self.name_timer = self.name_timer[:-1]
                self._render()
                return True
            if key == Qt.Key.Key_L:
                self.state = "timer_list"
                self._render()
            if key == Qt.Key.Key_Escape:
                self.timer.stop()
            else:
                self.name_timer += text
                self._render()
        elif self.state == 'timer_list':
            if key == Qt.Key.Key_Escape:
                self.state = "menu_input"
                self._render()
                return True
            if key == Qt.Key.Key_Return:
                self.state = "menu"
                self.stop("remove_nonewline")
                self._render()
                tuple(self.console.object['timer'].items())[self.selected_timer][1].show(False)
                return True
            if key == Qt.Key.Key_Up:
                self.selected_timer = max(0, self.selected_timer - 1)
                self._render()
                return True
            if key == Qt.Key.Key_Down:
                
                self.selected_timer = min(len(self.console.object['timer']) if self.console.object['timer'] else None, self.selected_timer + 1)
                self._render()
                return True
        # Timer input state handling
        elif self.state == 'input':
            if key == Qt.Key.Key_Return:
                # Process and start the timer
                for unit in ['h','m','s']:
                    self.timer_input = self.timer_input.replace(unit, "0")
                hours, mins, secs = map(int, self.timer_input.split(':'))
                self.time_left = (hours * 3600) + (mins * 60) + secs
                self.timer.start(1000)
                self.state = "running"
                self._render()
                return True
            else:
                # Handle digit input for time setting
                if text.isdigit():
                    for unit in ['h', 'm', 's']:
                        if unit in self.timer_input:
                            self.timer_input = self.timer_input.replace(unit, text, 1)
                            break
                    self._render()
            # Handle backspace for time input
            if key == Qt.Key.Key_Backspace:
                for i in reversed(range(len(self.timer_input))):
                    if self.timer_input[i].isdigit():
                        placeholder = ''
                        if i in [6, 7]:  # Seconds position
                            placeholder = 's'
                        elif i in [3, 4]:  # Minutes position
                            placeholder = 'm'
                        elif i in [0, 1]:  # Hours position
                            placeholder = 'h'
                        if placeholder:
                            self.timer_input = self.timer_input[:i] + placeholder + self.timer_input[i+1:]
                            break  
                self._render()

        # Timer running/paused state handling
        elif self.state in ('running', 'paused'):
            if key == Qt.Key.Key_Space:
                # Toggle pause state
                if self.state == 'running':
                    self.timer.stop()
                    self.state = 'paused'
                else:
                    self.timer.start(1000)
                    self.state = 'running'
                self._render()
                return True
            if key == Qt.Key.Key_R:
                # Reset timer to input state
                self.timer.stop()
                self.state = 'input'
                self.timer_input = "hh:mm:ss"
                self.time_left = 0
                self._render()
                return True
            if key == Qt.Key.Key_Alt:
                # Save timer to console's object storage
                if 'timer' not in self.console.object:
                    self.console.object['timer'] = {}
                self.console.object['timer'][self.name_timer] = self
                self.stop("hide")
                return True
        
        # Global escape key handling
        if key == Qt.Key.Key_Escape:
            self.stop()
            self.timer.stop()
            return True
        
        return True

    def _tick(self):
        """Handle timer countdown tick."""
        if self.time_left > 0:
            self.time_left -= 1
            if self.active:
                self._render()
        else:
            # Timer completion
            self.timer.stop()
            self.console.append("⏰ Time's up!")

class TimerCommand(Command):
    """Command to create and manage countdown timers."""
    
    def __init__(self):
        super().__init__()
        self.name = "timer"
        self.description = "Create and manage countdown timers"
        self.add_subcommand(TimerListCommand())
        self.register_argument()
        
    def register_argument(self):
        """Register command arguments."""
        self.add_argument(
            name="name",
            arg_type=ArgumentType.POSITIONAL,
            required=False,
            default=False,
            help="Name of existing timer to manage"
        )
    
    def execute_main(self, parse, appcontext):
        """Execute timer command logic.
        
        Args:
            parse: Parsed command input
            appcontext: Application context object
        """
        if parse['parse']['args']:
            # Access existing timer
            name_object = parse['parse']['args'][0]
            timer = appcontext.console.object['timer'][name_object]
            timer.show()
        else:
            # Create new timer
            timer = TimerWidget(appcontext.console)
            appcontext.console.widget = timer
            timer.show()

class TimerListCommand(Command):
    """Subcommand to list active timers."""
    
    def __init__(self):
        super().__init__()
        self.name = "list"
        self.description = "List active timers"
        self.is_subcommand = True
    
    def execute_main(self, parse, appcontext):
        """List all active timers.
        
        Args:
            parse: Parsed command input
            appcontext: Application context object
            
        Returns:
            Formatted list of active timers or message
        """
        list_timers = []
        if 'timer' in appcontext.console.object:
            for timer in appcontext.console.object['timer'].values():
                name = timer.name_timer
                hours = timer.time_left // 3600
                mins = (timer.time_left % 3600) // 60
                secs = (((timer.time_left % 3600) % 60) % 60)
                list_timers.append(f"{name} - {hours}:{mins}:{secs}")
            return "\n".join(list_timers)
        else:
            return "There are no active timers"