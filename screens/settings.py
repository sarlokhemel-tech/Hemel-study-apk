"""Settings Screen - General settings."""
from kivy.uix.screen import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.graphics import Color, RoundedRectangle
from core.theme_manager import ThemeManager, ThemeType
from core.app_manager import AppManager


class SettingsScreen(Screen):
    """Settings screen."""

    def __init__(self, **kwargs):
        """Initialize settings screen.

        Args:
            **kwargs: Additional arguments
        """
        super().__init__(**kwargs)
        self.theme_manager = ThemeManager.get_instance()
        self.app_manager = AppManager.get_instance()
        self.name = 'settings'

        main_layout = BoxLayout(orientation='vertical', spacing=10, padding=(10, 10))

        # Apply theme background
        with main_layout.canvas.before:
            Color(*self.theme_manager.get_color('background'))
            RoundedRectangle(
                size=main_layout.size,
                pos=main_layout.pos,
            )

        # Header
        header = BoxLayout(size_hint_y=None, height=50, spacing=10)
        back_btn = Button(
            text='← Back',
            size_hint_x=0.2,
            background_color=self.theme_manager.get_color('button_bg'),
        )
        back_btn.bind(on_press=self._on_back)
        header.add_widget(back_btn)

        title = Label(
            text='Settings',
            size_hint_x=0.8,
            color=self.theme_manager.get_color('text_primary'),
        )
        header.add_widget(title)
        main_layout.add_widget(header)

        # Settings scroll
        settings_scroll = ScrollView()
        settings_layout = GridLayout(
            cols=1,
            spacing=10,
            size_hint_y=None,
            padding=(10, 10),
        )
        settings_layout.bind(minimum_height=settings_layout.setter('height'))

        # Theme section
        theme_label = Label(
            text='Theme',
            size_hint_y=None,
            height=30,
            color=self.theme_manager.get_color('text_primary'),
            bold=True,
        )
        settings_layout.add_widget(theme_label)

        theme_spinner = Spinner(
            text=self.theme_manager.get_theme().value.capitalize(),
            values=self.theme_manager.get_available_themes(),
            size_hint_y=None,
            height=44,
        )
        theme_spinner.bind(text=self._on_theme_change)
        settings_layout.add_widget(theme_spinner)

        # Special Features button
        special_btn = Button(
            text='Special Feature & Settings',
            size_hint_y=None,
            height=50,
            background_color=self.theme_manager.get_color('primary'),
        )
        special_btn.bind(on_press=self._on_special_settings)
        settings_layout.add_widget(special_btn)

        # About section
        about_label = Label(
            text='About',
            size_hint_y=None,
            height=30,
            color=self.theme_manager.get_color('text_primary'),
            bold=True,
        )
        settings_layout.add_widget(about_label)

        about_text = Label(
            text='Hemel Study AI v1.0.0\nMade by Hemel\n\nA premium AI chat application with advanced features.',
            size_hint_y=None,
            height=80,
            color=self.theme_manager.get_color('text_secondary'),
        )
        settings_layout.add_widget(about_text)

        settings_scroll.add_widget(settings_layout)
        main_layout.add_widget(settings_scroll)

        self.add_widget(main_layout)

    def _on_theme_change(self, spinner, text: str) -> None:
        """Handle theme change.

        Args:
            spinner: Spinner instance
            text: Selected theme
        """
        theme = ThemeType(text.lower())
        self.theme_manager.set_theme(theme)

    def _on_special_settings(self, instance) -> None:
        """Open special settings."""
        self.app_manager.switch_screen('special_settings')

    def _on_back(self, instance) -> None:
        """Go back to chat screen."""
        self.app_manager.switch_screen('chat', direction='right')
