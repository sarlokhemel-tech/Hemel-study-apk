"""Main application entry point - Hemel Study AI."""
import logging
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.core.window import Window
from kivy.logger import Logger

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import core managers
from core.app_manager import AppManager
from core.theme_manager import ThemeManager
from core.settings_manager import SettingsManager
from core.storage_manager import StorageManager
from core.security_manager import SecurityManager

# Import screens
from screens.home import HomeScreen
from screens.chat import ChatScreen
from screens.history import HistoryScreen
from screens.settings import SettingsScreen
from screens.special_settings import SpecialSettingsScreen
from screens.theme_selection import ThemeSelectionScreen

# Window configuration
Window.size = (1080, 1920)
Window.left = 0
Window.top = 0


class HemelStudyAI(App):
    """Main Hemel Study AI application."""

    def __init__(self, **kwargs):
        """Initialize application.

        Args:
            **kwargs: Additional arguments
        """
        super().__init__(**kwargs)
        self.title = 'Hemel Study AI'
        self.icon = 'assets/icons/app_icon.png'
        self.theme_manager = None
        self.app_manager = None
        self.settings_manager = None
        self.storage_manager = None
        self.security_manager = None
        self.screen_manager = None
        self.chat_screen = None
        self.home_screen = None

    def build(self):
        """Build the application.

        Returns:
            Root widget
        """
        logger.info("Building Hemel Study AI application...")

        try:
            # Initialize managers
            self._initialize_managers()

            # Create screen manager
            self.screen_manager = ScreenManager(transition=FadeTransition())

            # Register screens
            self._register_screens()

            # Set initial screen
            self.screen_manager.current = 'home'

            logger.info("Application build completed successfully")
            return self.screen_manager

        except Exception as e:
            logger.error(f"Error building application: {e}")
            raise

    def _initialize_managers(self) -> None:
        """Initialize all core managers."""
        logger.info("Initializing core managers...")

        # Initialize security manager first (needed by other managers)
        self.security_manager = SecurityManager.get_instance()
        logger.info("Security manager initialized")

        # Initialize storage manager
        self.storage_manager = StorageManager.get_instance()
        self.storage_manager.initialize()
        logger.info("Storage manager initialized")

        # Initialize settings manager
        self.settings_manager = SettingsManager.get_instance()
        logger.info("Settings manager initialized")

        # Initialize theme manager
        self.theme_manager = ThemeManager.get_instance()
        logger.info("Theme manager initialized")

        # Initialize app manager
        self.app_manager = AppManager.get_instance()
        self.app_manager.initialize(self.screen_manager)
        logger.info("App manager initialized")

    def _register_screens(self) -> None:
        """Register all screens with screen manager."""
        logger.info("Registering screens...")

        # Home screen
        self.home_screen = HomeScreen(
            name='home',
            on_first_message=self._on_first_message
        )
        self.screen_manager.add_widget(self.home_screen)
        logger.info("Home screen registered")

        # Chat screen
        self.chat_screen = ChatScreen()
        self.screen_manager.add_widget(self.chat_screen)
        logger.info("Chat screen registered")

        # History screen
        history_screen = HistoryScreen()
        self.screen_manager.add_widget(history_screen)
        logger.info("History screen registered")

        # Settings screen
        settings_screen = SettingsScreen()
        self.screen_manager.add_widget(settings_screen)
        logger.info("Settings screen registered")

        # Special Settings screen
        special_settings_screen = SpecialSettingsScreen()
        self.screen_manager.add_widget(special_settings_screen)
        logger.info("Special settings screen registered")

        # Theme selection screen
        theme_screen = ThemeSelectionScreen()
        self.screen_manager.add_widget(theme_screen)
        logger.info("Theme selection screen registered")

    def _on_first_message(self, message: str) -> None:
        """Handle first message from user.

        Args:
            message: User message
        """
        logger.info("First message received, transitioning to chat...")
        
        # Start new chat
        self.chat_screen.start_new_chat()
        
        # Send the first message
        self.chat_screen._on_message_sent(message)
        
        # Switch to chat screen
        self.app_manager.switch_screen('chat', direction='left')

    def on_start(self):
        """Called when app starts."""
        logger.info("Application started")
        self.home_screen.animate_in()

    def on_stop(self):
        """Called when app stops."""
        logger.info("Application stopping...")
        
        try:
            # Shutdown managers
            if self.storage_manager:
                self.storage_manager.shutdown()
            if self.app_manager:
                self.app_manager.shutdown()
            
            logger.info("Application shutdown completed")
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")

    def on_pause(self):
        """Called when app is paused."""
        logger.info("Application paused")
        return True

    def on_resume(self):
        """Called when app resumes."""
        logger.info("Application resumed")


def main():
    """Main entry point."""
    logger.info("Starting Hemel Study AI...")
    app = HemelStudyAI()
    app.run()


if __name__ == '__main__':
    main()
