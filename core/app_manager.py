"""Application Manager - Handles app lifecycle and global state."""
import logging
from typing import Optional, Dict, Any, Callable, List
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.clock import Clock

logger = logging.getLogger(__name__)


class AppManager:
    """Manages application lifecycle, state, and screen transitions."""

    _instance: Optional['AppManager'] = None

    def __init__(self):
        """Initialize AppManager singleton."""
        self.screen_manager: Optional[ScreenManager] = None
        self.current_screen: Optional[Screen] = None
        self.app_state: Dict[str, Any] = {}
        self.observers: Dict[str, List[Callable]] = {}
        self.is_running: bool = False

    @classmethod
    def get_instance(cls) -> 'AppManager':
        """Get singleton instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def initialize(self, screen_manager: ScreenManager, window_width: int = 1080, window_height: int = 1920) -> None:
        """Initialize app manager with screen manager.

        Args:
            screen_manager: Kivy ScreenManager instance
            window_width: Default window width
            window_height: Default window height
        """
        self.screen_manager = screen_manager
        Window.size = (window_width, window_height)
        self.is_running = True
        logger.info("AppManager initialized")

    def set_state(self, key: str, value: Any) -> None:
        """Set application state value.

        Args:
            key: State key
            value: State value
        """
        self.app_state[key] = value
        self._notify_observers(key, value)
        logger.debug(f"State changed: {key} = {value}")

    def get_state(self, key: str, default: Any = None) -> Any:
        """Get application state value.

        Args:
            key: State key
            default: Default value if key not found

        Returns:
            State value or default
        """
        return self.app_state.get(key, default)

    def subscribe(self, key: str, callback: Callable) -> None:
        """Subscribe to state changes.

        Args:
            key: State key to observe
            callback: Callback function(value)
        """
        if key not in self.observers:
            self.observers[key] = []
        self.observers[key].append(callback)
        logger.debug(f"Observer subscribed to {key}")

    def _notify_observers(self, key: str, value: Any) -> None:
        """Notify all observers of state change.

        Args:
            key: State key
            value: New value
        """
        if key in self.observers:
            for callback in self.observers[key]:
                try:
                    callback(value)
                except Exception as e:
                    logger.error(f"Observer callback error: {e}")

    def switch_screen(self, screen_name: str, direction: str = 'left') -> None:
        """Switch to different screen.

        Args:
            screen_name: Name of screen to switch to
            direction: Animation direction ('left', 'right', 'up', 'down')
        """
        if self.screen_manager is None:
            logger.error("ScreenManager not initialized")
            return

        try:
            self.screen_manager.transition.direction = direction
            self.screen_manager.current = screen_name
            self.current_screen = self.screen_manager.get_screen(screen_name)
            logger.info(f"Switched to screen: {screen_name}")
        except Exception as e:
            logger.error(f"Error switching screen: {e}")

    def get_current_screen(self) -> Optional[Screen]:
        """Get current active screen.

        Returns:
            Current Screen or None
        """
        return self.current_screen

    def add_screen(self, screen: Screen, name: str) -> None:
        """Add screen to manager.

        Args:
            screen: Screen instance
            name: Screen name
        """
        if self.screen_manager is not None:
            self.screen_manager.add_widget(screen)
            screen.name = name
            logger.info(f"Screen added: {name}")

    def shutdown(self) -> None:
        """Shutdown application."""
        self.is_running = False
        self.app_state.clear()
        self.observers.clear()
        logger.info("AppManager shutdown complete")

    def reset_state(self) -> None:
        """Reset all application state."""
        self.app_state.clear()
        logger.info("Application state reset")

    def is_initialized(self) -> bool:
        """Check if app is initialized.

        Returns:
            True if initialized
        """
        return self.screen_manager is not None and self.is_running
