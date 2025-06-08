from src.modules.command import Command, ArgumentType
from src.modules.widgets.widget import Widget
from PyQt6.QtGui import QTextCursor, QKeyEvent
from PyQt6.QtCore import Qt, QTimer

class StopwatchWidget(Widget):
    
    def __init__(self, console):

        super().__init__(console)
        # Widget states: 'menu_input', 'timer_list', 'running', 'paused'
        self.state = 'menu_input'
        self.elapsed = 0.0

        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self._tick)

        self.active = True
        self.name_stopwatch = fr"#{0 if 'stopwatch' not in self.console.object else len(self.console.object['stopwatch'])}"
        
        self.selected_stopwatch = 0
        # Text formatting for different widget states
        self.formats = {
            'menu_input': self._create_format("#00F2FF", "#525554"),
            'stopwatch_list': self._create_format("#7CFE4C", "#D8D8D8"),
            'stopwatch_list selected': self._create_format("#F2F7F0", "#3BFB00"),
            'running': self._create_format("#000000", "#00FF00"),
            'paused': self._create_format("#000000", "#FFFF00")
        }
    
    def _render(self):
        """Render the timer interface based on current state."""
        self._clear()
        cursor = self.console.textCursor()
        cursor.setPosition(self.get_start_pos())
        
        if self.state == 'menu_input':
            cursor.insertText(f"Stopwatch\n", self.formats['menu_input'])
            cursor.insertText(f"Enter a name for the stopwatch: {self.name_stopwatch}_\n", self.formats['menu_input'])
            cursor.insertText("[Enter] Create a new stopwatch [L] List stopwatchs [Esc] Cancel", self.formats['menu_input'])
        
        elif self.state == 'stopwatch_list':
            if 'stopwatch' in self.console.object:
                for count, stopwatch in enumerate(self.console.object['stopwatch'].values()):
                    name = stopwatch.name_stopwatch
                    hours = stopwatch.elapsed // 3600
                    mins = (stopwatch.elapsed % 3600) // 60
                    secs = (((stopwatch.elapsed % 3600) % 60) % 60)
                    if count == self.selected_stopwatch:
                        cursor.insertText(f"{name} - {hours}:{mins}:{secs}\n", self.formats['stopwatch_list selected'])
                    else:
                        cursor.insertText(f"{name} - {hours}:{mins}:{secs}\n", self.formats['stopwatch_list'])
            else:
                cursor.insertText(f"There are no active stopwatch\n", self.formats['stopwatch_list'])
            cursor.insertText("[Enter] Select stopwatch [Esc] Cancel", self.formats['stopwatch_list'])
                
        elif self.state in ('running', 'paused'):
            total = int(self.elapsed)
            hours = total // 3600
            mins = (total % 3600) // 60
            secs = (((total % 3600) % 60) % 60)
            deci = int((self.elapsed - total) * 10)
            fmt = self.formats['running'] if self.state == 'running' else self.formats['paused']
            cursor.insertText(f"Stopwatch {self.name_stopwatch}: {hours:02d}:{mins:02d}:{secs:02d}.{deci}\n", fmt)
            cursor.insertText("[Space] Pause/Resume  [R] Reset  [Alt] Swipe the stopwatch  [Esc] Exit", fmt)
        
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
                self.state = "running"
                self.timer.start()
                self._render()
                return True
            if key == Qt.Key.Key_Backspace:
                self.name_stopwatch = self.name_stopwatch[:-1]
                self._render()
                return True
            if key == Qt.Key.Key_L:
                self.state = "stopwatch_list"
                self._render()
            if key == Qt.Key.Key_Escape:
                self.timer.stop()
            else:
                self.name_stopwatch += text
                self._render()
        elif self.state == 'stopwatch_list':
            if key == Qt.Key.Key_Escape:
                self.state = "menu_input"
                self._render()
                return True
            if key == Qt.Key.Key_Return:
                self.state = "menu"
                self.stop("remove_nonewline")
                self._render()
                tuple(self.console.object['stopwatch'].items())[self.selected_stopwatch][1].show(False)
                return True
            if key == Qt.Key.Key_Up:
                self.selected_stopwatch = max(0, self.selected_stopwatch - 1)
                self._render()
                return True
            if key == Qt.Key.Key_Down:
                
                self.selected_stopwatch = min(len(self.console.object['stopwatch']) if self.console.object['stopwatch'] else None, self.selected_stopwatch + 1)
                self._render()
                return True
        # Timer running/paused state handling
        elif self.state in ('running', 'paused'):
            if key == Qt.Key.Key_Space:
                # Toggle pause state
                if self.state == 'running':
                    self.timer.stop()
                    self.state = 'paused'
                else:
                    self.timer.start()
                    self.state = 'running'
                self._render()
                return True
            if key == Qt.Key.Key_R:
                # Reset timer to input state
                self.elapsed = 0.0
                self._render()
                return True
            if key == Qt.Key.Key_Alt:
                # Save timer to console's object storage
                if 'stopwatch' not in self.console.object:
                    self.console.object['stopwatch'] = {}
                self.console.object['stopwatch'][self.name_stopwatch] = self
                self.stop("hide")
                return True
        
        # Global escape key handling
        if key == Qt.Key.Key_Escape:
            self.stop()
            self.timer.stop()
            return True
        
        return True

    def _tick(self):
        if self.active:
            self._render()
        self.elapsed += 0.1
        

class StopwatchCommand(Command):
    """Command to create and manage countdown timers."""
    
    def __init__(self):
        super().__init__()
        self.name = "s"
        self.description = ""
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
            stopwatch = appcontext.console.object['stopwatch'][name_object]
            stopwatch.show()
        else:
            # Create new timer
            stopwatch = StopwatchWidget(appcontext.console)
            appcontext.console.widget = stopwatch
            stopwatch.show()

# class TimerListCommand(Command):
#     """Subcommand to list active timers."""
    
#     def __init__(self):
#         super().__init__()
#         self.name = "list"
#         self.description = "List active timers"
#         self.is_subcommand = True
    
#     def execute_main(self, parse, appcontext):
#         """List all active timers.
        
#         Args:
#             parse: Parsed command input
#             appcontext: Application context object
            
#         Returns:
#             Formatted list of active timers or message
#         """
#         list_timers = []
#         if 'timer' in appcontext.console.object:
#             for timer in appcontext.console.object['timer'].values():
#                 name = timer.name_timer
#                 hours = timer.time_left // 3600
#                 mins = (timer.time_left % 3600) // 60
#                 secs = (((timer.time_left % 3600) % 60) % 60)
#                 list_timers.append(f"{name} - {hours}:{mins}:{secs}")
#             return "\n".join(list_timers)
#         else:
#             return "There are no active timers"