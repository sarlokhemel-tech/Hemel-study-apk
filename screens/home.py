"""Home Screen - Welcome interface."""
from kivy.uix.screen import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.graphics import Color, RoundedRectangle
from typing import Optional, Callable
from core.app_manager import AppManager
from core.theme_manager import ThemeManager
from widgets.input_bar import InputBar


class HomeScreen(Screen):
    """Home screen with welcome interface."""

    def __init__(self, on_first_message: Optional[Callable] = None, **kwargs):
        """Initialize home screen.

        Args:
            on_first_message: Callback when first message is sent
            **kwargs: Additional arguments
        """
        super().__init__(**kwargs)
        self.on_first_message = on_first_message
        self.app_manager = AppManager.get_instance()
        self.theme_manager = ThemeManager.get_instance()
        self.name = 'home'

        # Main layout
        main_layout = BoxLayout(orientation='vertical', spacing=20)

        # Apply theme background
        with main_layout.canvas.before:
            Color(*self.theme_manager.get_color('background'))
            RoundedRectangle(
                size=main_layout.size,
                pos=main_layout.pos,
            )

        # Welcome container (centered)
        welcome_container = BoxLayout(
            orientation='vertical',
            size_hint_y=0.7,
            spacing=20,
            padding=(20, 0),
        )

        # Title
        self.title_label = Label(
            text='Hemel Study AI',
            font_size='48sp',
            bold=True,
            size_hint_y=None,
            height=100,
            color=self.theme_manager.get_color('primary'),
        )
        welcome_container.add_widget(Label(size_hint_y=0.3))
        welcome_container.add_widget(self.title_label)

        # Subtitle
        self.subtitle_label = Label(
            text='Made by Hemel',
            font_size='18sp',
            size_hint_y=None,
            height=40,
            color=self.theme_manager.get_color('text_secondary'),
        )
        welcome_container.add_widget(self.subtitle_label)
        welcome_container.add_widget(Label(size_hint_y=0.3))

        main_layout.add_widget(Label(size_hint_y=0.1))
        main_layout.add_widget(welcome_container)
        main_layout.add_widget(Label(size_hint_y=0.1))

        # Input bar
        self.input_bar = InputBar(send_callback=self._on_first_message)
        main_layout.add_widget(self.input_bar)

        self.add_widget(main_layout)
        self.main_layout = main_layout

        # Subscribe to theme changes
        self.theme_manager.subscribe(self._on_theme_change)

    def _on_first_message(self, message: str) -> None:
        """Handle first message sent.

        Args:
            message: Message text
        """
        if message and self.on_first_message:
            # Animate out welcome text
            self._animate_welcome_out()
            self.on_first_message(message)

    def _animate_welcome_out(self) -> None:
        """Animate welcome text out of view."""
        anim = Animation(opacity=0, duration=0.5)
        anim.start(self.title_label)
        anim.start(self.subtitle_label)

    def animate_in(self) -> None:
        """Animate welcome screen in."""
        self.title_label.opacity = 0
        self.subtitle_label.opacity = 0
        
        anim1 = Animation(opacity=1, duration=0.6)
        anim1.start(self.title_label)
        
        anim2 = Animation(opacity=1, duration=0.8)
        anim2.start(self.subtitle_label)

    def _on_theme_change(self, theme) -> None:
        """Handle theme change.

        Args:
            theme: New theme
        """
        # Update colors
        self.title_label.color = self.theme_manager.get_color('primary')
        self.subtitle_label.color = self.theme_manager.get_color('text_secondary')

        # Update background
        with self.main_layout.canvas.before:
            self.main_layout.canvas.clear()
            Color(*self.theme_manager.get_color('background'))
            RoundedRectangle(
                size=self.main_layout.size,
                pos=self.main_layout.pos,
            )

    def on_enter(self) -> None:
        """Called when screen is displayed."""
        self.animate_in()
