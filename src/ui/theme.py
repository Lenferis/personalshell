import sys
import json
from pathlib import Path
from typing import Dict, Any, List
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit
from PyQt6.QtGui import (QTextCursor, QFont, QKeyEvent, QColor, 
                         QPalette, QFontDatabase, QTextOption)
import yaml

class Theme:
    def __init__(self, name, data):
        self.name = name
        self.data = data

default_theme = {
    'font': {
        'family': 'Consolas',
        'size': 10,
        'weight': 300,
        'italic': False
    },
    'colors': {
        'background': '#000000',
        'color':'#FFFFFF',
        'selection_color': '#464040'
    },
    'scrollbar':{
        'background': '#282828',
        'width': 10,
        'margin': 0,
        'background_handle': '#FFFFFF',
        'height_handle': 10,
        'border_radius_handle': 0
    },
    'border': '0px black solid',
    'padding': '0px',
    'border_radius': '0px'
}
class ThemeApplier:
    def __init__(self, widget: QTextEdit):
        self.widget = widget
        self._loaded_fonts = set()

    def apply_theme(self, theme_data: dict) -> None:
        theme_data = theme_data.data
        self._apply_font(theme_data)
        self._apply_stylesheet(theme_data)

    def _apply_font(self, theme_data: dict) -> None:
        """Настраивает шрифт виджета"""
        font_data = theme_data.get('font')
        font = QFont()
        font_family = font_data.get('family', default_theme['font']['family'])
        font.setFamily(font_family)
        font.setPointSize(font_data.get('size', default_theme['font']['size']))
        
        font.setWeight(font_data.get('weight', default_theme['font']['weight']))
        font.setItalic(font_data.get('italic', default_theme['font']['italic']))
        self.widget.setFont(font)

    def _apply_stylesheet(self, theme_data: dict) -> None:
        styles = []

        colors = theme_data.get('colors', {})
        styles.extend([
            f"background: {colors.get('background', default_theme['colors']['background'])}",
            f"color: {colors.get('color', default_theme['colors']['color'])}",
            f"selection-background-color: {colors.get('selection_color', default_theme['colors']['selection_color'])}"
        ])

        styles.extend([
            f"border: {theme_data.get('border', default_theme['border'])}",
            f"padding: {theme_data.get('padding', default_theme['padding'])}",
            f"border-radius: {theme_data.get('border_radius', default_theme['border_radius'])}"
        ])

        scrollbar = theme_data.get('scrollbar', {})
        scrollbar_style = f"""
            QScrollBar:vertical {{
                background: {scrollbar.get('background', default_theme['scrollbar']['background'])};
                width: {scrollbar.get('width', default_theme['scrollbar']['width'])}px;
                margin: {scrollbar.get('margin', default_theme['scrollbar']['margin'])}px;
            }}
            QScrollBar::handle:vertical {{
                background: {scrollbar.get('background_handle', default_theme['scrollbar']['background_handle'])};
                min-height: {scrollbar.get('height_handle', default_theme['scrollbar']['height_handle'])}px;
                border-radius: {scrollbar.get('border_radius_handle', default_theme['scrollbar']['border_radius_handle'])}px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: none;
            }}
        """

        stylesheet = f"""
            QTextEdit {{
                {'; '.join(styles)};
            }}
            {scrollbar_style}
        """
        self.widget.setStyleSheet(stylesheet)


class ThemeLoader:
    def __init__(self, config: Dict):
        self.config = config

        self.theme_paths = [Path(p).absolute() for p in config.data['paths']['theme']]
        self.overrides = config.data['user']['theme'].get('override', {})
        self.loaded_themes = {}
    def load_all_themes(self):
        for path in self.theme_paths:
            if not path.exists():
                continue
                
            for theme_file in path.glob("*.yaml"):
                with open(theme_file, 'r') as f:
                    data = yaml.safe_load(f)
                    if data['meta']['name'] in self.config.data['user']['theme']['available']:
                        self._process_theme(data)
        return self.loaded_themes

    def _process_theme(self, data):
        theme_name = data['meta']['name']
        if theme_name in self.loaded_themes:
            return

        # Обработка наследования
        if 'base' in data:
            if data['base'] not in self.loaded_themes:
                base_theme = self._load_base_theme(data['base'])
                self.loaded_themes.update(base_theme)
            
            base_data = self.loaded_themes[data['base']].data
            merged = self._merge_dicts(base_data, data)
            data = merged

        # Применение переопределений из конфига
        data = self._merge_dicts(data, self.overrides)
        self.loaded_themes[theme_name] = Theme(theme_name, data)

    def _load_base_theme(self, base_name):
        for path in self.theme_paths:
            theme_file = path / f"{base_name}.yaml"
            if theme_file.exists():
                with open(theme_file) as f:
                    data = yaml.safe_load(f)
                    return {data['name']: Theme(data['name'], data)}
        return {}

    def _merge_dicts(self, base, new):
        merged = base.copy()
        for key, value in new.items():
            if isinstance(value, dict) and key in base:
                merged[key] = self._merge_dicts(base[key], value)
            else:
                merged[key] = value
        return merged





class ThemeManager:
    def __init__(self, config: Dict, widget):
        self.loader = ThemeLoader(config)
        self.applier = ThemeApplier(widget=widget)
        self.themes = self.loader.load_all_themes()
        self.current_theme: dict = None

    def list_themes(self) -> List[str]:
        return self.themes

    def get_theme(self, name: str) -> dict:
        return self.themes.get(name).data

    def set_theme(self, name: str) -> bool:
        if theme := self.themes.get(name):
            self.current_theme = theme
            self.applier.apply_theme(self.current_theme)
            return True
        return False        
