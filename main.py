import sys, os
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import Qt
from pathlib import Path

from ui.console import Console

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyLine")
        self.setCentralWidget(Console())
        self.resize(800, 400)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()



# # config/prod.yaml
# # ==============================================
# #               Basic settings
# # ==============================================
# app:
#   name: "PyLine"
#   version: "0.5.0"
#   env: "production"                 # prod|stage|dev|test
#   debug: false                      # Режим отладки
#   maintenance_mode: false           # Технические работы

# # ==============================================
# #               Paths and directories
# # ==============================================
# paths:
#   commands:
#     - "./src/pccl/commands"           # Основные команды
#     - "plugins"                     # Внешние плагины
#   logs: "./logs"
#   session: "./session"
#   theme:
#     - "./theme"

# # ==============================================
# #               Logging
# # ==============================================
# logging:
#   level: "INFO"                     # DEBUG|INFO|WARNING|ERROR|CRITICAL
#   rotation:
#     max_size: "10MB"
#     backup_count: 7
#     compress: true
#   format: "%(asctime)s | %(levelname)-8s | %(module)s: %(message)s"

# # ==============================================
# #              Localization
# # ==============================================
# locale:
#   language: "en_US"                  # ru_RU|es_ES|fr_FR...
#   timezone: "UTC"
#   datetime_format: "iso"             # iso|custom
#   units_system: "metric"             # metric|imperial

# # ==============================================
# #            Modules and Plugins
# # ==============================================
# modules:
#   core:
#     - "commands.essentials.env"
#     - "commands.essentials.meta"
#     - "commands.essentials.output"
#     - "commands.essentials.sctrl"
#     - "commands.theme.theme"
  
#   plugins:
#     - " "
# # ==============================================
# #             Custom Settings
# # ==============================================
# user:
#   theme:
#     current: "dark-matrix"           # Имя активной темы
#   shortcuts:
#     command_search: "Ctrl+K"
#     history: "Ctrl+H"
#   history_size: 1000                 # Максимум записей истории
#   auto_update: true theme
