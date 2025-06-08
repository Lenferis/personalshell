from src.modules.command import Command, ArgumentType
from src.modules.widgets.widget import Widget
from PyQt6.QtWidgets import QApplication, QTextEdit, QCalendarWidget
from PyQt6.QtGui import QTextCursor, QTextCharFormat, QColor, QKeyEvent
from PyQt6.QtCore import Qt, QDate
import calendar
from datetime import datetime
class CalendarWidget(Widget):
    
    def __init__(self, console):
        """
        Initialize timer widget with default state and configurations.
        
        Args:
            console: Reference to console object for interaction
        """
        super().__init__(console)
    
        self.date = QDate.currentDate()
        self.active = True

        self.formats = {
            'header': self._create_format("#00F2FF"),
            'weekdays': self._create_format("#11BE48"),
            'normal': self._create_format("#F6F6F6"),
            'selected': self._create_format("#D1FF04", "#80D8BB")
        }
    
    def _render(self):
        """Render the timer interface based on current state."""
        self._clear()
        cursor = self.console.textCursor()
        cursor.setPosition(self.get_start_pos())

        year = self.date.year()
        month = self.date.month()
        day = self.date.day()
        

        cursor.insertText(f"Calendar: {year}-{month:02d}\n", self.formats['header'])
        weekheader = ["Mo","Tu","We","Th","Fr","Sa","Su"]
        for wd in weekheader:
            cursor.insertText(fr"{wd} ", self.formats['weekdays'])
        cursor.insertText("\n")

        first_day = QDate(year, month, 1)
        start_column = (first_day.dayOfWeek() - 1) % 7
        
        day_count = first_day.daysInMonth()
        day_num = 1
        column = 0

        # Пустые ячейки до 1 числа
        for _ in range(start_column):
            cursor.insertText("   ")
            column += 1

        while day_num <= day_count:
            date = QDate(year, month, day_num)
            fmt = self.formats['selected'] if day_num == day else self.formats['normal']
            text = f"{day_num:2d} "
            cursor.insertText(text, fmt)

            column += 1
            if column >= 7:
                cursor.insertText("\n")
                column = 0

            day_num += 1

        self.console.setTextCursor(cursor)

    def handle_key(self, event: QKeyEvent) -> bool:
        key = event.key()
        if key == Qt.Key.Key_Escape:
            self.stop("remove")
            return True
        elif key == Qt.Key.Key_Left:
            self.date = self.date.addDays(-1)
            self._render()
            return True
        elif key == Qt.Key.Key_Right:
            self.date = self.date.addDays(1)
            self._render()
            return True
        elif key == Qt.Key.Key_Up:
            self.date = self.date.addDays(-7)
            self._render()
            return True
        elif key == Qt.Key.Key_Down:
            self.date = self.date.addDays(7)
            self._render()
            return True
        elif key == Qt.Key.Key_Return:
            self.stop("remove")
            return True
        return False
        

    
    def __init__(self):
        super().__init__()
        self.name = "calendar"
        self.description = ""
    
    def execute_main(self, parse, appcontext):
        """Execute timer command logic.
        
        Args:
            parse: Parsed command input
            appcontext: Application context object
        """
       
        calendar = CalendarWidget(appcontext.console)
        appcontext.console.widget = calendar
        calendar.show()

