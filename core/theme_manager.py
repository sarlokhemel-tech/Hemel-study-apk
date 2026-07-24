"""Theme Manager - Handles application theming."""
import logging
import json
from typing import Dict, Tuple, Optional
from pathlib import Path
from enum import Enum

logger = logging.getLogger(__name__)


class ThemeType(Enum):
    """Available themes."""
    LIGHT = "light"
    DARK = "dark"
    WHATSAPP = "whatsapp"


class ThemeManager:
    """Manages application themes and colors."""

    _instance: Optional['ThemeManager'] = None
    _config_dir = Path.home() / '.hemel_study_ai'
    _theme_file = _config_dir / 'theme.json'

    # Color definitions
    THEMES = {
        ThemeType.LIGHT: {
            'background': (0.95, 0.95, 0.95, 1),
            'primary': (0.2, 0.4, 0.9, 1),
            'secondary': (0.1, 0.7, 0.8, 1),
            'text_primary': (0.1, 0.1, 0.1, 1),
            'text_secondary': (0.5, 0.5, 0.5, 1),
            'surface': (1, 1, 1, 1),
            'user_bubble': (0.2, 0.4, 0.9, 1),
            'ai_bubble': (0.9, 0.9, 0.9, 1),
            'input_bg': (1, 1, 1, 1),
            'button_bg': (0.2, 0.4, 0.9, 1),
            'button_text': (1, 1, 1, 1),
            'divider': (0.85, 0.85, 0.85, 1),
        },
        ThemeType.DARK: {
            'background': (0.13, 0.13, 0.13, 1),
            'primary': (0.3, 0.6, 1, 1),
            'secondary': (0.2, 0.85, 0.95, 1),
            'text_primary': (0.95, 0.95, 0.95, 1),
            'text_secondary': (0.7, 0.7, 0.7, 1),
            'surface': (0.17, 0.17, 0.17, 1),
            'user_bubble': (0.3, 0.6, 1, 1),
            'ai_bubble': (0.25, 0.25, 0.25, 1),
            'input_bg': (0.25, 0.25, 0.25, 1),
            'button_bg': (0.3, 0.6, 1, 1),
            'button_text': (0.13, 0.13, 0.13, 1),
            'divider': (0.3, 0.3, 0.3, 1),
        },
        ThemeType.WHATSAPP: {
            'background': (0.09, 0.12, 0.13, 1),
            'primary': (0, 0.6, 0.3, 1),
            'secondary': (0, 0.7, 0.4, 1),
            'text_primary': (0.95, 0.95, 0.95, 1),
            'text_secondary': (0.75, 0.75, 0.75, 1),
            'surface': (0.13, 0.16, 0.17, 1),
            'user_bubble': (0, 0.5, 0.25, 1),
            'ai_bubble': (0.22, 0.28, 0.29, 1),
            'input_bg': (0.13, 0.16, 0.17, 1),
            'button_bg': (0, 0.6, 0.3, 1),
            'button_text': (0.95, 0.95, 0.95, 1),
            'divider': (0.2, 0.25, 0.26, 1),
        },
    }

    def __init__(self):
        """Initialize ThemeManager singleton."""
        self.current_theme = ThemeType.DARK
        self.observers = []
        self._load_saved_theme()

    @classmethod
    def get_instance(cls) -> 'ThemeManager':
        """Get singleton instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _load_saved_theme(self) -> None:
        """Load previously saved theme from storage."""
        try:
            if self._theme_file.exists():
                with open(self._theme_file, 'r') as f:
                    data = json.load(f)
                    theme_name = data.get('theme', 'dark')
                    self.current_theme = ThemeType(theme_name)
                    logger.info(f"Theme loaded: {theme_name}")
            else:
                self._save_theme()
        except Exception as e:
            logger.error(f"Error loading theme: {e}")
            self.current_theme = ThemeType.DARK

    def _save_theme(self) -> None:
        """Save current theme to storage."""
        try:
            self._config_dir.mkdir(parents=True, exist_ok=True)
            with open(self._theme_file, 'w') as f:
                json.dump({'theme': self.current_theme.value}, f)
            logger.info(f"Theme saved: {self.current_theme.value}")
        except Exception as e:
            logger.error(f"Error saving theme: {e}")

    def set_theme(self, theme: ThemeType) -> None:
        """Set current theme.

        Args:
            theme: ThemeType to set
        """
        self.current_theme = theme
        self._save_theme()
        self._notify_observers()
        logger.info(f"Theme changed to: {theme.value}")

    def get_theme(self) -> ThemeType:
        """Get current theme.

        Returns:
            Current ThemeType
        """
        return self.current_theme

    def get_color(self, color_key: str) -> Tuple[float, float, float, float]:
        """Get color for current theme.

        Args:
            color_key: Color key name

        Returns:
            RGBA tuple
        """
        try:
            return self.THEMES[self.current_theme][color_key]
        except KeyError:
            logger.warning(f"Color key not found: {color_key}, using default")
            return (1, 1, 1, 1)

    def get_colors(self) -> Dict[str, Tuple[float, float, float, float]]:
        """Get all colors for current theme.

        Returns:
            Dictionary of colors
        """
        return self.THEMES[self.current_theme].copy()

    def subscribe(self, callback) -> None:
        """Subscribe to theme changes.

        Args:
            callback: Function to call on theme change
        """
        self.observers.append(callback)

    def _notify_observers(self) -> None:
        """Notify all observers of theme change."""
        for callback in self.observers:
            try:
                callback(self.current_theme)
            except Exception as e:
                logger.error(f"Observer callback error: {e}")

    def get_available_themes(self) -> list:
        """Get list of available themes.

        Returns:
            List of ThemeType values
        """
        return [theme.value for theme in ThemeType]
