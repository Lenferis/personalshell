import sys, os
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import Qt
from pathlib import Path

from src.ui.console import Console

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("personalshell")
        self.setCentralWidget(Console())
        self.resize(800, 400)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

