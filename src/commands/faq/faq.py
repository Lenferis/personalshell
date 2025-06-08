from src.modules.command import Command, ArgumentType
from src.modules.widgets.widget import Widget
from PyQt6.QtGui import QTextCursor, QKeyEvent
from PyQt6.QtCore import Qt, QTimer

FAQ_ENTRIES = [
    ("How to run the application?", "Run `python main.py` in terminal."),
    ("How to add a task?", "Press A on calendar, enter description and press Enter."),
    ("How to change theme?", "Type `themes` command and select theme from list."),
    ("How to view roadmap?", "Type `roadmap` command and select stage."),
    ("How to exit widget?", "Press Esc to close current widget."),
    ("Basic navigation", "Use ↑/↓ arrows to navigate, Enter to select, Esc to exit"),
    ("Command help", "Type `help` to see available commands"),
    ("Save data", "All data is automatically saved in JSON format"),
    ("Keyboard shortcuts", 
     "A: Add task\n"
     "D: Delete item\n"
     "E: Edit item\n"
     "S: Save manually\n"
     "/: Search mode"),
    ("Report bug", "Please create issue on GitHub repository with detailed description")
]


class FAQWidget(Widget):
    """
    Interactive FAQ widget for displaying and searching frequently asked questions.
    
    Features:
    - Browse FAQ entries with keyboard navigation
    - Search functionality
    - Detailed answer view
    
    States:
    - 'default': Browsing mode
    - 'search': Text input for search
    - 'answer': Viewing full answer
    """

    def __init__(self, console):
        """
        Initialize FAQ widget with default state and configurations.
        
        Args:
            console: Reference to console object for interaction
        """
        super().__init__(console)
        # Widget states: 'default', 'search', 'answer'
        self.state = 'default'
        self.entries = FAQ_ENTRIES
        self.selected = 0  # Currently selected FAQ index
        self.search_text = ""  # Current search query
        self.filtered = self.entries  # Entries filtered by search

        # Text formatting configurations
        self.formats = {
            'title': self._create_format("#00FFFF"),
            'normal': self._create_format("#00FF00"),
            'selected': self._create_format("#000000", "#00FF00"),
            'status': self._create_format("#AAAAAA"),
            'input': self._create_format("#00FFFF")
        }

    def _render(self):
        """Render FAQ interface based on current state."""
        self._clear()
        cursor = self.console.textCursor()
        cursor.setPosition(self.get_start_pos())
        
        if self.state == "answer":
            # Display detailed answer view
            question, answer = self.filtered[self.selected]
            cursor.insertText(f"=== FAQ - {question} ===\n", self.formats['title'])
            cursor.insertText(answer)
            cursor.insertText("\n(Enter/Esc exit answer)\n", self.formats['status'])
        else:
            # Display main FAQ list
            cursor.insertText("=== FAQ (press / to search) ===\n", self.formats['title'])
            
            if self.state == "search":
                # Show search input
                cursor.insertText(f"Search: {self.search_text}_\n", self.formats['input'])
                # Filter entries based on search text
                items = [e for e in self.entries if self.search_text.lower() in e[0].lower()]
            else:
                items = self.entries
                
            self.filtered = items
            
            # Display FAQ list
            for i, (q, a) in enumerate(self.filtered):
                fmt = self.formats['selected'] if (self.active and i == self.selected) else self.formats['normal']
                prefix = '>' if (self.active and i == self.selected) else ' '
                cursor.insertText(f"{prefix} {q}\n", fmt)
            
            # Display navigation help
            help_text = "\n(↑/↓ navigate, Enter show answer, / search, Esc exit)\n"
            cursor.insertText(help_text, self.formats['status'])
            
        self.console.setTextCursor(cursor)

    def handle_key(self, event):
        """
        Handle keyboard input for FAQ navigation and interaction.
        
        Args:
            event: Qt key event object
            
        Returns:
            True if key was handled, False otherwise
        """
        if not self.active:
            return False
        
        key = event.key()
        text = event.text()
        
        # Answer view controls
        if self.state == "answer":
            if key in (Qt.Key.Key_Escape, Qt.Key.Key_Return):
                self.state = "default"
                self._render()
                return True
        
        # Search mode controls
        elif self.state == "search":
            if key == Qt.Key.Key_Escape:
                self.state = "default"
                self._render()
                return True
            elif key == Qt.Key.Key_Backspace:
                self.search_text = self.search_text[:-1]
                self._render()
                return True
            elif key == Qt.Key.Key_Return and self.filtered:
                self.state = "answer"
                self._render()
            elif text:
                self.search_text += text
                self._render()
        
        # Default mode controls
        else:
            if key == Qt.Key.Key_Slash:
                self.state = "search"
                self.search_text = ""
                self.selected = 0
                self._render()
                return True
            elif key == Qt.Key.Key_Up:
                self.selected = max(0, self.selected - 1)
                self._render()
            elif key == Qt.Key.Key_Down:
                self.selected = min(len(self.filtered) - 1, self.selected + 1)
                self._render()
            elif key == Qt.Key.Key_Return and self.filtered:
                self.state = "answer"
                self._render()
            elif key == Qt.Key.Key_Escape:
                self.stop("remove")
                return True
        
        return True


class FAQCommand(Command):
    """
    Command to open interactive FAQ widget.
    
    Aliases:
    - 'helpfaq'
    - 'questions'
    - 'faqs'
    """
    
    def __init__(self):
        super().__init__()
        self.name = "faq"
        self.aliases = ["helpfaq", "questions", "faqs"]
        self.description = "Open interactive FAQ with common questions and answers"

    def execute_main(self, parse, appcontext):
        """
        Execute FAQ command to show interactive FAQ widget.
        
        Args:
            parse: Parsed command input
            appcontext: Application context object
        """
        # Create and show FAQ widget
        faq = FAQWidget(appcontext.console)
        appcontext.console.widget = faq 
        faq.show()