from modules.command import Command, ArgumentType
from modules.widgets.widget import Widget
from PyQt6.QtGui import QTextCursor, QMouseEvent, QColor, QTextCharFormat, QKeyEvent
from PyQt6.QtCore import Qt, QTimer

class TimerWidget(Widget):
    def __init__(self, console):
        super().__init__(console)
        self.state = 'menu_input'  # 'input', 'running', 'paused', menu_input, list timer
        self.time_left = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self._tick)
        self.timer_input = "hh:mm:ss"
        self.active = True


        self.name_timer = fr"#{0 if 'timer' not in self.console.object else len(self.console.object['timer'])}"


        self.formats = {
            'menu_input': self._create_format("#00F2FF", "#525554"),
            'timer_list': self._create_format("#7CFE4C", "#D8D8D8"),
            'timer_list selected': self._create_format("#F2F7F0", "#3BFB00"),
            'input': self._create_format("#FFFFFF", "#333333"),
            'running': self._create_format("#000000", "#00FF00"),
            'paused': self._create_format("#000000", "#FFFF00")
        }
    def _render(self):
        self._clear()
        cursor = self.console.textCursor()
        cursor.setPosition(self.get_start_pos())
        if self.state == 'menu_input':
            cursor.insertText(f"Timers\n", self.formats['menu_input'])
            cursor.insertText(f"Enter a name for the timer: {self.name_timer}_\n", self.formats['menu_input'])
            cursor.insertText("[Enter] Create a new timer [L] List timers [Esc] Cancel", self.formats['menu_input'])
        if self.state == 'timer_list':
            if 'timer' in self.console.object:
                for timer in self.console.object['timer'].values():
                    name = timer.name_timer
                    hours = timer.time_left // 3600
                    mins = (timer.time_left % 3600) // 60
                    secs = (((timer.time_left % 3600) % 60) % 60)
                    cursor.insertText(f"{name} - {hours}:{mins}:{secs}\n", self.formats['input'])
            else:
                cursor.insertText(f"There are no active timers\n", self.formats['input'])
            cursor.insertText("[Enter] Select timer [Esc] Cancel\n", self.formats['input'])
                
        if self.state == 'input':
            cursor.insertText(f"Timer {self.name_timer}\n", self.formats['input'])
            cursor.insertText(f"Set Timer (hh:mm:ss): {self.timer_input}\n", self.formats['input'])
            cursor.insertText("[Enter] Start  [Esc] Cancel\n", self.formats['input'])
        if self.state in ('running', 'paused'):
            hours = self.time_left // 3600
            mins = (self.time_left % 3600) // 60
            secs = (((self.time_left % 3600) % 60) % 60)

            fmt = self.formats['running'] if self.state == 'running' else self.formats['paused']
            cursor.insertText(f"Timer {self.name_timer}: {hours}:{mins}:{secs}\n", fmt)
            cursor.insertText("[Space] Pause/Resume  [R] Reset  [Alt] Swipe the timer  [Esc] Exit", fmt)
        self.console.setTextCursor(cursor)

    def handle_key(self, event):
        if not self.active:
            return False
        
        key = event.key()
        text = event.text()

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




        if self.state == 'input':
            if key == Qt.Key.Key_Return:
                for unit in ['h','m','s']:
                    self.timer_input = self.timer_input.replace(unit, "0")
                hours, mins, secs = map(int, self.timer_input.split(':'))
                self.time_left = (hours * 3600) + (mins * 60) + secs
                self.timer.start(1000)
                self.state = "running"
                self._render()
                return True
            else:
                if text.isdigit():
                    for unit in ['h', 'm', 's']:
                        if unit in self.timer_input:
                            self.timer_input = self.timer_input.replace(unit, text, 1)
                            break
                    self._render()
            if key == Qt.Key.Key_Backspace:
                for i in reversed(range(len(self.timer_input))):
                    if self.timer_input[i].isdigit():
                        placeholder = ''
                        if i in [6, 7]:  
                            placeholder = 's'
                        elif i in [3, 4]:  
                            placeholder = 'm'
                        elif i in [0, 1]:  
                            placeholder = 'h'
                        if placeholder:
                            self.timer_input = self.timer_input[:i] + placeholder + self.timer_input[i+1:]
                            break  
                self._render()





        elif self.state in ('running', 'paused'):
            if key == Qt.Key.Key_Space:
                if self.state == 'running':
                    self.timer.stop()
                    self.state = 'paused'
                else:
                    self.timer.start(1000)
                    self.state = 'running'
                self._render()
                return True
            if key == Qt.Key.Key_R:
                self.timer.stop()
                self.state = 'input'
                self.timer_input = "hh:mm:ss"
                self.time_left = 0
                self._render()
                return True
            if key == Qt.Key.Key_Alt:
                if 'timer' not in self.console.object:
                    self.console.object['timer'] = {}
                self.console.object['timer'][self.name_timer] = self
                print(self.console.object['timer'])
                self.stop("hide")
                return True
        if key == Qt.Key.Key_Escape:
            self.stop()
            return True
        return True

    def _tick(self):
        if self.active:
            if self.time_left > 0:
                self.time_left -= 1
                self._render()
            else:
                self.timer.stop()
                self.console.append("⏰ Time's up!")



class TimerCommand(Command):
    def __init__(self):
        super().__init__()
        self.name = "timer"
        self.description = ""
        self.add_subcommand(TimerListCommand())
        self.register_argument()
        
    def register_argument(self):
        self.add_argument(
            name="name object",
            arg_type=ArgumentType.POSITIONAL,
            required=False,
            default=False,
            help="Timer name object"
        )
    def execute_main(self, parse, appcontext):
        if parse['parse']['args']:
            name_object = parse['parse']['args'][0]
            timer = appcontext.console.object['timer'][name_object]
            appcontext.console.widget = timer
            timer.show()
        else:
            timer = TimerWidget(appcontext.console)
            appcontext.console.widget = timer
            timer.show()

class TimerListCommand(Command):
    def __init__(self):
        super().__init__()
        self.name = "list"
        self.description = ""
    def execute_main(self, parse, appcontext):
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
        